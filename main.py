from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import psycopg2
from psycopg2 import sql

# Replace with your bot token
TOKEN = 'YOUR_BOT_TOKEN'


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Use /create_db <dbname> <user> <password> to create a new database.')


def create_db(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 3:
        update.message.reply_text('Usage: /create_db <dbname> <user> <password>')
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

        update.message.reply_text(f'Database {dbname} and user {dbuser} created successfully!')

    except Exception as e:
        update.message.reply_text(f'An error occurred: {e}')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("create_db", create_db))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
