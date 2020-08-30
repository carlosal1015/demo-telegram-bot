#!usr/bin/env python


from logging import getLogger, basicConfig, INFO
from os import environ, getenv
from sys import exit
from random import randint
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
load_dotenv()
# Configurar Logging
basicConfig(
    level = INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = getLogger()

# Solicitar TOKEN
TOKEN = getenv("TOKEN")
mode = getenv("MODE")

if mode == "dev":
    # Acceso Local (desarrollo)
    def run(updater):
        updater.start_polling()
        print("BOT CARGADO")
        updater.idle() # Permite finalizar el bot con Ctrl + C.
elif mode == "prod":
    # Acceso HEROKU (producción)
    def run(updater):
        PORT = int(environ.get("PORT", "8443"))
        HEROKU_APP_NAME = environ.get("HEROKU_APP_NAME")
        updater.start_webook(listen = "0.0.0.0", port = PORT, url_path = TOKEN)
        updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
else:
    logger.info("No se especificó el MODE.")
    exit()

def start(update, context):
    logger.info(f"El usuario {update.effective_user['username']}, ha iniciado una conversación.")
    name = update.effective_user['first_name']
    update.message.reply_text(f"Hola {name} yo soy tu bot.")

def random_number(update, context):
    user_id = update.effective_user['id']
    logger.info(f"El usuario {user_id}, ha solicitado un número aleatorio")
    number = randint(0, 10)
    context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=f"<b>Número</b> aleatorio:\n{number}")

def echo(update, context):
    user_id = update.effective_user['id']
    logger.info("El usuario {user_id}, ha enviado un mensaje de texto.")
    text = update.message.text
    context.bot.sendMessage(
        chat_id=user_id,
        parse_mode= "MarkdownV2",
        text=f"**Escribiste:**\n_{text}_"
    )

if __name__ == "__main__":
    # Obtenemos información de nuestro bot
    my_bot = Bot(token = TOKEN)
    #print(my_bot.get_me())

# Enlazamos nuestro updater con nuestro bot
updater = Updater(my_bot.token, use_context=True)

# Creamos despachador
dp = updater.dispatcher

# Creamos los manejadores
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("random", random_number))
dp.add_handler(MessageHandler(Filters.text, echo))

run(updater)