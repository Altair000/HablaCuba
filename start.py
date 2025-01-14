import telebot
import os
from flask import Flask, request
from cc_gen import main
from autokey import chk

TOKEN = '7698270668:AAGb1rPBU27IlMH_vmTMFpLzAE9slnSFonk'
nombre_proyecto = os.getenv("REPL_SLUG")
nombre_usuario = os.getenv("REPL_OWNER")
if nombre_proyecto and nombre_usuario:
    WEBHOOK_URL = f"https://{nombre_proyecto}.{nombre_usuario}.repl.co"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Variables para almacenar datos de entrada del usuario
bin_format = None
month = None
year = None
n = None
chat_id = None

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    success = bot.set_webhook(url=WEBHOOK_URL + f'/{TOKEN}')
    if success:
        return 'Webhook configurada correctamente', 200
    else:
        return 'Fallo al configurar el webhook', 500

@app.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    bot.delete_webhook()
    return 'Webhook eliminada correctamente', 200

# Manejo de comandos y respuestas
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Usa /chk para comenzar')

@bot.message_handler(commands=['chk'])
def start_collecting_data(message):
    global chat_id
    chat_id = message.chat.id
    bot.reply_to(message, 'Por favor, ingresa el BIN:')
    bot.register_next_step_handler(message, get_bin)

def get_bin(message):
    global bin_format
    bin_format = message.text
    bot.reply_to(
        message,
        'Ahora ingresa el Mes (como un número, por ejemplo, 10) o en caso aleatorio ingrese 00: '
    )
    bot.register_next_step_handler(message, get_month)

def get_month(message):
    global month
    try:
        month = int(message.text)
        bot.reply_to(
            message,
            'Ingresa el **Año** (por ejemplo, 2025) o en caso aleatorio ingrese 00: '
        )
        bot.register_next_step_handler(message, get_year)
    except ValueError:
        bot.reply_to(message, 'Por favor, ingresa un mes válido. Intenta de nuevo.')
        bot.register_next_step_handler(message, get_month)

def get_year(message):
    global year
    try:
        year = int(message.text)
        bot.reply_to(message, 'Ingresa la **Cantidad** de tarjetas a generar:')
        bot.register_next_step_handler(message, get_quantity)
    except ValueError:
        bot.reply_to(message, 'Por favor, ingresa un año válido. Intenta de nuevo.')
        bot.register_next_step_handler(message, get_year)

def get_quantity(message):
    global month, year, n
    try:
        n = int(message.text)
        if month == 00:
            month = None
        if year == 00:
            year = None
        # Llamar a la función principal con los datos recopilados
        main(bin_format, month, year, n)
        chk(chat_id, bot)

        # Reiniciar variables para el próximo uso
        reset_variables()
    except ValueError:
        bot.reply_to(message, 'Por favor, ingresa una cantidad válida. Intenta de nuevo.')
        bot.register_next_step_handler(message, get_quantity)

def reset_variables():
    global bin_format, month, year, n, chat_id
    bin_format = None
    month = None
    year = None
    n = None
    chat_id = None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443)
