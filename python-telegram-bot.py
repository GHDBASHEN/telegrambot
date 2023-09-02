import logging
import threading
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackContext

from bgremove import RemoveBackgroundAPI
import logging

TOKEN='6462562581:AAGfBxogF8Sued8_b92PbvZeWvMduXgXd-Y'
bg_token='r81DhiPxt8HaSJGFPv82vJQD'

async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm Lucil, please talk to me!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="What do you want to know?")

async def request_image(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please send the image you want to remove the background from.")

async def bgremove(update: Update, context: CallbackContext):
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    if file is not None:

        await file.download_to_drive("input_image.jpg")

        remove_bg_api = RemoveBackgroundAPI(bg_token)
        remove_bg_api.remove_background('input_image.jpg', output_path='output_image.png')
        with open('output_image.png', 'rb') as image_file:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_file)
    else:
        await request_image(update, context)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    remove_handler = CommandHandler('remove', request_image)
    bgremove_handler = MessageHandler(filters.PHOTO, bgremove)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(remove_handler)
    application.add_handler(bgremove_handler)

    application.run_polling()
