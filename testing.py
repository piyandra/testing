import telebot


app = telebot.TeleBot("6459247934:AAFSllqletBf9sdYB91NXzldQCiw9qG-B7I")

import requests

ipaddress = requests.get('https://ipinfo.io/json').json()['ip']


@app.message_handler(commands=['start'])
async def start(message):
    app.reply_to(message, text="Bot Ini Digunakan Untuk Generate Postgresql\nWelcome! Use /create_db <dbname> <user> <password> to create a new database.")

@app.message_handler(commands=['create_db'])
async def create_db(message):
