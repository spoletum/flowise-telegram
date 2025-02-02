import os
from dotenv import load_dotenv
from flowise import Flowise, PredictionData
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

global flowiseClient
global chatflowId

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user    
    await update.message.reply_markdown_v2(
        fr"Hi {user.mention_markdown_v2()}\!",
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle a message."""

    # Extract the session id from the message
    session_id = update.message.from_user.id

    # Create a prediction
    response = flowiseClient.create_prediction(PredictionData(question=update.message.text, chatflowId=chatflowId, streaming=False, chatId=session_id))
    # Extract text from the response
    response_text = ""
    for item in response:
        response_text += item["text"]
    # Escape special characters for markdown v2
    await update.message.reply_text(response_text)

if __name__ == "__main__":

    # Load environment variables
    load_dotenv()

    # Setup the Flowise client
    FLOWISE_API_KEY = os.getenv("FLOWISE_API_KEY")
    FLOWISE_API_URL = os.getenv("FLOWISE_API_URL")
    chatflowId = os.getenv("FLOWISE_CHATFLOW_ID")
    if not FLOWISE_API_KEY:
        raise ValueError("FLOWISE_API_KEY not found in environment variables")
    if not FLOWISE_API_URL:
        raise ValueError("FLOWISE_API_URL not found in environment variables")
    if not chatflowId:
        raise ValueError("FLOWISE_CHATFLOW_ID not found in environment variables")
    
    flowiseClient = Flowise(base_url=FLOWISE_API_URL, api_key=FLOWISE_API_KEY)

    # Setup the Telegram bot
    TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
    if not TELEGRAM_API_KEY:
        raise ValueError("TELEGRAM_API_KEY not found in environment variables")
    application = Application.builder().token(TELEGRAM_API_KEY).build()
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Run the bot
    application.run_polling()
