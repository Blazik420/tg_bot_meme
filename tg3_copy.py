import os
import random
import telebot
import json

api_code = '####'
# Initialize your bot with the API token
bot = telebot.TeleBot(api_code)


MEMES_DIR = 'C:/Users/vital/Desktop/TG BOT/memes'
jsonpath = "C:/Users/vital/Desktop/TG BOT/json"
USER_INFO_FILE = os.path.join(jsonpath, 'user_info.json')


if not os.path.exists(MEMES_DIR):
    os.makedirs(MEMES_DIR)
user_dir = 'C:/Users/vital/Desktop/TG BOT/user_memes'
user_memes = {}
if os.path.exists(USER_INFO_FILE):
    with open(USER_INFO_FILE, 'r') as f:
        user_memes = json.load(f)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Дарова кент! Нажми /help, чтобы узнать все команды")


@bot.message_handler(commands=['help'])
def handle_help(message):
    help_message = "Available commands:\n" \
                   "/start - Start the bot\n" \
                   "/help - Get help\n" \
                   "/info - Get information\n" \
                   "/status - Get status\n" \
                   "/meme - Get a meme\n\n" \
                   "всем ку\n" \
                   "Если вы хотите отправить мем, просто отправьте его боту. я рассмотрю мем и выложу его в случае надобности"
    bot.reply_to(message, help_message)


@bot.message_handler(commands=['info'])
def handle_info(message):
    bot.reply_to(message, "Мемы и предложка. Все в одном")


@bot.message_handler(commands=['status'])
def handle_status(message):
    bot.reply_to(message, "Бот работает")


ADMIN_USER_IDS = [1918737583]  # Replace with your own admin user IDs

@bot.message_handler(content_types=['photo'], func=lambda message: message.from_user.id not in ADMIN_USER_IDS)
def handle_default_user_image(message):
    user_id = message.from_user.id

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    image = bot.download_file(file_info.file_path)

    default_user_memes_dir = os.path.join(user_dir, 'default_user_memes')
    if not os.path.exists(default_user_memes_dir):
        os.makedirs(default_user_memes_dir)

    image_name = f"user_meme_{user_id}_{file_id}.jpg"  # You can generate a unique name for the image
    image_path = os.path.join(default_user_memes_dir, image_name)
    with open(image_path, 'wb') as new_image:
        new_image.write(image)

    user_memes.setdefault(str(user_id), []).append(image_name)
    with open(USER_INFO_FILE, 'w') as f:
        json.dump(user_memes, f)

    bot.reply_to(message, "Мем получен. я посмотрю его и обязательно выложу если он крутой)")

@bot.message_handler(content_types=['photo'], func=lambda message: message.from_user.id in ADMIN_USER_IDS)
def handle_admin_image(message):
    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    image = bot.download_file(file_info.file_path)
    
    image_name = f"admin_meme_{file_id}.jpg"  # You can generate a unique name for the image
    image_path = os.path.join(MEMES_DIR, image_name)
    with open(image_path, 'wb') as new_image:
        new_image.write(image)

    user_memes.setdefault(str(user_id), []).append(image_name)

    with open(USER_INFO_FILE, 'w') as f:
        json.dump(user_memes, f)
    bot.reply_to(message, "Мем добавлен")

# Для простых юзеров отдельные функции для предложки
@bot.message_handler(content_types=['photo'])
def handle_user_image(message):
    bot.reply_to(message, "Мем получен. я посмотрю его и обязательно выложу если он крутой)")


#Можно получить мем
@bot.message_handler(commands=['meme'])
def handle_meme(message):
    user_id = message.from_user.id

    # Если все посмотрел - сказать что мемы кончились
    meme_files = os.listdir(MEMES_DIR)
    if user_id in user_memes and len(user_memes[user_id]) >= len(meme_files):
        bot.reply_to(message, "Ты все посмотрел, возвращайся позже, герой")
        return
    meme_files = os.listdir(MEMES_DIR)
    unseen_memes = [meme for meme in meme_files if meme not in user_memes.get(str(user_id), [])]
    if not unseen_memes:
        bot.reply_to(message, "Ты все посмотрел, возвращайся позже, герой")
        return

    # Рандомный мем из еще не просмотренных
    random_meme = random.choice(unseen_memes)

    # Отправить мем
    meme_path = os.path.join(MEMES_DIR, random_meme)
    with open(meme_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

    # Сделать апдейт списка
    user_memes.setdefault(str(user_id), []).append(random_meme)

    with open(USER_INFO_FILE, 'w') as f:
        json.dump(user_memes, f)

bot.polling()
