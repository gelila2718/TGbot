import requests
import telebot
from bs4 import BeautifulSoup
from tabulate import tabulate
from PIL import Image
from io import BytesIO
import random

telegram_bot_token = '6924678579:AAHnmzqbC1XsRrGvhg1sqY1H2eiKubENWu0'
channel_id = '-1002131859663'  # Update this with your channel username or ID

bot = telebot.TeleBot(telegram_bot_token)

# Define categories for options
categories = ['Fashion', 'Property', 'Electronics', 'Vehicles']

# Create ReplyKeyboardMarkup with categories as options
keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard.add(
    *[telebot.types.KeyboardButton(category) for category in categories])


def scrape_website(url, category):
  response = requests.get(url)
  if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    if category.lower() == 'fashion':
      fashion_list = soup.find_all('div', class_='masonry-item')[:8]
      random.shuffle(fashion_list)
      fashion_data = [(item.find('img')['src'], item.text.strip())
                      for item in fashion_list]
      return fashion_data
    elif category.lower() == 'property':
      property_list = soup.find_all('div', class_='masonry-item')[:8]
      random.shuffle(property_list)
      property_data = [(item.find('img')['src'], item.text.strip())
                       for item in property_list]
      return property_data
    elif category.lower() == 'electronics':
      electronics_list = soup.find_all('div', class_='masonry-item')[:8]
      random.shuffle(electronics_list)

      electronics_data = [(item.find('img')['src'], item.text.strip())
                          for item in electronics_list]
      return electronics_data
    elif category.lower() == 'vehicles':
      vehicles_list = soup.find_all('div', class_='masonry-item')[:8]
      random.shuffle(vehicles_list)
      vehicles_data = [(item.find('img')['src'], item.text.strip())
                       for item in vehicles_list]
      return vehicles_data
  else:
    print(f"Failed to fetch data from {url}")
    return []


def send_to_channel(message):
  max_length = 4000
  if len(message) <= max_length:
    bot.send_message(channel_id, message)
  else:
    chunks = [
        message[i:i + max_length] for i in range(0, len(message), max_length)
    ]
    for chunk in chunks:
      bot.send_message(channel_id, chunk)


def send_images_with_text(images_data):
  for img_url, text in images_data:
    try:
      response = requests.get(img_url)
      img_data = response.content
      img = Image.open(BytesIO(img_data))
      # Convert image to bytes for sending it through Telegram
      img_byte_array = BytesIO()
      img.save(img_byte_array, format='PNG')
      img_byte_array.seek(0)
      # Send image with text
      bot.send_photo(channel_id, img_byte_array, caption=text)
    except Exception as e:
      print(f"Error displaying image from {img_url}: {e}")


@bot.message_handler(func=lambda message: True)
def select_category(message):
  if message.text in categories:
    category = message.text
    send_to_channel(f"New updates in {category}:")

    if category.lower() in ['fashion', 'property', 'electronics', 'vehicles']:
      if category.lower() == 'fashion':
        data = scrape_website('https://jiji.com.et/clothing', category)
      elif category.lower() == 'property':
        data = scrape_website('https://jiji.com.et/new-builds', category)
      elif category.lower() == 'electronics':
        data = scrape_website(
            'https://jiji.com.et/accessories-and-supplies-for-electronics',
            category)
      elif category.lower() == 'vehicles':
        data = scrape_website('https://jiji.com.et/cars', category)

      if data:
        send_images_with_text(data)
      else:
        send_to_channel(f"No {category} updates found.")
    else:
      send_to_channel("Invalid category.")
  else:
    bot.send_message(message.chat.id,
                     "Please select a category:",
                     reply_markup=keyboard)


bot.polling(True)
