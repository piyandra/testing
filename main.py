import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ApplicationBuilder
import psycopg2
from psycopg2 import sql

# Replace with your bot token
TOKEN = '6459247934:AAFSllqletBf9sdYB91NXzldQCiw9qG-B7I'
ip = requests.get('https://ipinfo.io/json').json()['ip']


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome! Use /create_db <dbname> <user> <password> to create a new database.')


async def create_db(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 3:
        await update.message.reply_text('Usage: /create_db <dbname> <user> <password>')
        return

    dbname, dbuser, dbpass = context.args

    try:
        # Connect to the PostgreSQL server
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgres',
            host='localhost'
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Create database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))

        # Create user and grant privileges
        cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(dbuser)), [dbpass])
        cursor.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(sql.Identifier(dbname), sql.Identifier(dbuser)))

        await update.message.reply_text(f'Database {dbname} dan user {dbuser} berhasil dibuat!')
        await update.message.reply_text(f'Connection String \n<code>postgres://{dbuser}:{dbpass}@{ip}:5432/{dbname}</code>', parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f'An error occurred: {e}')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    db_handler = CommandHandler('create_db', create_db)
    application.add_handler(start_handler)
    application.add_handler(db_handler)
    application.run_polling()
