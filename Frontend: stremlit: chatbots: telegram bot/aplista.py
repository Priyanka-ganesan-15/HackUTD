import asyncio
import nest_asyncio
import openai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
from credentials import API_KEY, SAMBANOVA_API_KEY  # Add SAMBANOVA_API_KEY to your credentials.py

# Apply nest_asyncio to fix event loop issues
nest_asyncio.apply()

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=SAMBANOVA_API_KEY,
    base_url="https://api.sambanova.ai/v1",
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi! I am an AI assistant powered by Llama. Send me any message and I will respond!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process messages through Llama API and respond."""
    try:
        # Send "typing" action while processing
        await update.message.chat.send_action("typing")
        
        # Get the response from Llama
        response = client.chat.completions.create(
            model='Meta-Llama-3.1-8B-Instruct',
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": update.message.text}
            ],
            temperature=0.1,
            top_p=0.1
        )
        
        # Extract and send the response
        ai_response = response.choices[0].message.content
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        error_message = f"Sorry, I encountered an error: {str(e)}"
        await update.message.reply_text(error_message)
        print(f"Error processing message: {str(e)}")

async def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(API_KEY).build()

    # Add command handler for /start
    application.add_handler(CommandHandler("start", start_command))
    
    # Add message handler to process messages through Llama
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    print('Bot is running with Llama AI integration...')
    await application.initialize()
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())