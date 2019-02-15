import os
import logging 
import atexit
import markovify
from telegram.ext import Updater, CommandHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def ping(update, context):
    update.message.reply_text("pong")

def shitpost(model, update, context):
    text = None
    while text is None:
        text = model.make_short_sentence(140)
    update.message.reply_text(text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def start(bot_token, main_chat_id, model):
    u = Updater(bot_token, use_context=True)

    u.dispatcher.add_handler(CommandHandler("ping", ping))
    u.dispatcher.add_handler(CommandHandler(
        "shitpost", lambda update, context: shitpost(model, update, context),
        filters=Filters.chat(int(main_chat_id))))
    u.dispatcher.add_error_handler(error)

    logger.info("Polling for updates")
    u.start_polling()

@atexit.register
def on_shutdown():
    logger.info('Shutting down')

if __name__ == '__main__':
    bot_token = os.environ["BOT_TOKEN"]
    main_chat_id = os.environ["MAIN_CHAT_ID"]
    model_path = os.environ["MODEL_PATH"]

    logger.info("Loading the S H I T P O S T model")

    with open(model_path) as f:
        model_json = f.read()

    model = markovify.Text.from_json(model_json)

    logger.info("Starting the bot")
    
    start(bot_token, main_chat_id, model)
