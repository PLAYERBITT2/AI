import logging
import requests
from transformers import pipeline
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram bot token (replace with your own token from BotFather)
API_TOKEN = '7235646357:AAEFqhtbZhYIxxKywRoqI85IZZwY42M70k8'

# Load a pre-trained GPT model from Hugging Face for conversational AI
chatbot = pipeline("text-generation", model="gpt2")

def generate_response(query):
    """
    Generate a response using the GPT-2 model.
    """
    response = chatbot(query, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']

def google_search(query):
    """
    Use Google Search API (SerpApi) to get top search results.
    Replace 'YOUR_SERPAPI_KEY' with your SerpApi API key.
    """
    api_key = "YOUR_SERPAPI_KEY"  # Replace with your SerpApi API Key
    search_url = f"https://serpapi.com/search?q={query}&api_key={api_key}"

    # Send a request to the Google search API
    response = requests.get(search_url)
    search_results = response.json()

    # Extract and return the top result from the search
    if 'organic_results' in search_results:
        top_result = search_results['organic_results'][0]['snippet']
        return top_result
    else:
        return "No relevant results found."

def hybrid_ai(query):
    """
    Determine if the query is informational or conversational.
    If it's a question (contains '?'), use Google search. Otherwise, use GPT-2 for a conversation.
    """
    if "?" in query:
        # If the query contains a question mark, assume it's informational
        return google_search(query)
    else:
        # Otherwise, treat it as a conversation
        return generate_response(query)

def start(update: Update, context: CallbackContext):
    """
    Command handler for /start command.
    """
    update.message.reply_text("Hello! I am your AI assistant. Ask me anything!")

def help(update: Update, context: CallbackContext):
    """
    Command handler for /help command.
    """
    update.message.reply_text("You can ask me questions or chat with me. Type anything to begin.")

def handle_message(update: Update, context: CallbackContext):
    """
    Handle incoming messages and generate AI responses.
    """
    user_input = update.message.text  # Get the text from the message
    response = hybrid_ai(user_input)  # Get AI's response (either Google search or GPT-2)
    update.message.reply_text(response)  # Send the response back to the user

def main():
    # Set up the bot and updater
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Set up logging to track errors
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    # Add message handler for handling text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
