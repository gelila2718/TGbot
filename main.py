import requests
import time
import telebot
from bs4 import BeautifulSoup
from tabulate import tabulate  # Added import for tabulate

telegram_bot_token = '6950136624:AAHloC-eobxzHQWFjJycAF3qJNQo33pOjVM'
bot = telebot.TeleBot(telegram_bot_token)
telegram_channel_username = '@WebScraped_Gelila_bot'

# Dictionary to keep track of users who have opened the bot for the first time
first_time_users = {}

@bot.message_handler(commands=['start'])
def get_update(message):
    user_id = message.from_user.id

    if user_id not in first_time_users:
        # User is opening the bot for the first time
        first_time_users[user_id] = True
        bot.send_message(message.chat.id, f"Welcome, {message.from_user.first_name}! This is the Web Scraping Bot. Type /start to interact.")
    else:
        # User has opened the bot before
        bot.send_message(message.chat.id, "Welcome back!")

    # Fetch and send job titles (limit to 10)
    response = requests.get("https://www.booksiteethiopia.com")
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id='content')

    if results:
        new_data = results.find_all('li', class_='product')  # Corrected variable name
        new_data = new_data[:10]

        if new_data:
            new_data_list = [job.text for job in new_data]
            job_table = tabulate([(index + 1, title) for index, title in enumerate(new_data_list)], headers=['No.', 'book title price and rating'], tablefmt='grid')
            bot.send_message(message.chat.id, f"top 10 books from etehiopian site :\n{job_table}")
        else:
            bot.send_message(message.chat.id, "No updates found.")
    else:
        bot.send_message(message.chat.id, "Unable to fetch data from the website.")

bot.polling()