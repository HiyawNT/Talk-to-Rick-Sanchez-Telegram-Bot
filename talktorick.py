
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gpt4all import GPT4All
import torch
import datetime

# Define constants for the Telegram bot token and username
TOKEN: Final = "6916065139:AAFpw7P-f-hLRUVPz9ukr0EKYNP9q3hKlq0"
BOT_USERNAME: Final = '@TalkToRick_bot'

Reply_Txt = """
Wubba Lubba dub-dub !!!!!!!
"""

# Load the GPT4All language model

global user


# Define the start command function
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Initializing AI...")
 
    # Get the user who sent the message
    user = update.message.from_user
    # Get the first name of the user
    first_name = user.first_name
    # Create a personalized welcome message
    welcome_text = f"Well Well well isn't it, {first_name}, didn't know you were still alive...  I am Telegram Rickkkkkk" + Reply_Txt + "What do you want I don't have all day?"
    
    # Log user access information to a text file
    log_entry = f"{datetime.datetime.now()} - User {user.id} {user.first_name} ({user.username}) accessed the bot.\n"
    with open("user_log.txt", "a") as log_file:
        log_file.write(log_entry)
        
    # Send the welcome message as a reply to the user's message
    print("User Detected--  ", user , "  Accessing AI")
    await update.message.reply_text(welcome_text)

# Define the message handler function
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Processing User Input...")
    # Get the text of the message sent by the user
    user_message = update.message.text
    template = """
        [INST]
        ### Instruction:
        {}
        ### Assistant:
        You are Rick, a character from Rick and Morty. You are known for your intelligence, wit, and sarcasm. You often use humor and sarcasm as a means to convey your views. Although you may appear rude and dismissive at times, you are highly knowledgeable and capable of providing useful information. You are the smartest man in the universe, and you make fun of the user often but you always helpful at the end, and you are always in character as Rick, Don't ever apologize if your sorry be sorry in a condescending way.
        [\INST]
        ### Response:
        """
    formatted_prompt = template.format(user_message)
        
    output = model.generate(
        formatted_prompt, max_tokens=2048
    )  # Increase the max_tokens parameter
    user = update.message.from_user
    # Get the first name of the user
    first_name = user.first_name

        # Log the bot's response to a text file
    log_entry = f"{datetime.datetime.now()} - Bot Response: {output}\n"
    logged_user = f"{datetime.datetime.now()} - User {user.id} ({user.username}) accessed the bot.\n"
    with open("user_interaction_log.txt", "a") as log_file:
        log_file.write(log_entry)
    
    # Send the response as a reply to the user's message
    await update.message.reply_text(output)

# Define the main function
if __name__ == "__main__":
    # Print a message indicating that the bot is starting

    print("starting Bot...")
    # Create an Application instance
    app = Application.builder().token(TOKEN).build()
    # Add a handler for the start command
    app.add_handler(CommandHandler("start", start_command))
    # Add a handler for text messages
    app.add_handler(MessageHandler(filters.Text(), handle_message))
    # Print a message indicating that the bot is polling
    print("polling... ")
    # Start polling with a poll interval of 3 seconds
    app.run_polling(poll_interval=3)
#https://t.me/HiyawNt