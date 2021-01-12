import logging
from flask import Flask,request
from telegram import Bot, Update
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters, Dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN="1384518922:AAFzTmpii3aDXgtpmu0pa9kh_NyFEUl-ZIU"
app=Flask(__name__)

@app.route('/')
def index():
    return "Hello!"

@app.route(f'/{TOKEN}',methods={'GET','POST'})
def webhook():
    """webhook view which receive updates from telegram"""
    update=Update.de_json(request.get_json(),bot)
    #process update
    dp.process_update(update)
    return "ok"

def start(bot, update):
    print(update)
    author=update.message.from_user.first_name
    reply="Hi! {}".format(author)
    bot.send_message(chat_id=update.message.chat_id,text = reply)


def help(bot, update):
    help_txt="This is a help text"
    bot.send_message(chat_id=update.message.chat_id,text = help_txt)

def echo_text(bot, update):
    echo_txt=update.message.text
    bot.send_message(chat_id=update.message.chat_id,text = echo_txt)

def echo_sticker(bot, update):
    echo_txt=update.message.text
    bot.send_sticker(chat_id=update.message.chat_id,sticker = update.message.sticker.file_id)

def error(bot,update):
    logger.error("Update '%s' caused error '%s'",update, update.error)




if __name__=="__main__":
    bot=Bot(TOKEN)
    bot.set_webhook("https://ceeeb7b9887a.ngrok.io/"+TOKEN)
    dp=Dispatcher(bot,None)

    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("help",help))
    dp.add_handler(MessageHandler(Filters.text,echo_text))
    dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
    dp.add_error_handler(error)


    app.run(port=8443)
