import telebot
import requests
from telebot import types

TOKEN = '1839712189:AAE1M-6l2owoRIRy72S0r1wleZE7z1O8GIE'

WEATHER_TOKEN = 'cc2d757656721c7838f819f150c7f7e6'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help','weather','profile','calc'])
def start_bot(message):
    if message.text.lower() == '/start':
        bot.send_message(message.chat.id, "Привет!\n Я такойто такойтович бот.")

    elif message.text.lower() == '/help':
        bot.send_message(message.chat.id, "Помощь")
        
    elif message.text.lower() == '/weather':
        bot.send_message(message.chat.id, "Вы попали в раздел погоды")
        bot.send_message(message.chat.id, "Введите название города")
        bot.register_next_step_handler(message,weather_menu)
    
    elif message.text.lower() == '/profile':
        bot.send_message(message.chat.id, "Вы попали в профиль")
        bot.send_message(message.chat.id, "Как вас зовут?")
        bot.register_next_step_handler(message, entry_name)
    
    elif message.text.lower() == '/calc':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сумма')
        btn2 = types.KeyboardButton('Минус')
        keyboard.add(btn1)
        keyboard.add(btn2)
        
        bot.send_message(message.chat.id, "Калькулятор")
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=keyboard)
        bot.register_next_step_handler(message, calc_start)

def calc_start(message):
    bot.send_message(message.chat.id, "Введите два числа через пробел")
    if message.text == 'Сумма':
        bot.register_next_step_handler(message, calc_sum)
        

def calc_sum(message):
    nums = message.text.split()
    num1 = int(nums[0])
    num2 = int(nums[1])
    bot.send_message(message.chat.id, f"Сумма: {num1 + num2}")
# имя, возраст, номер телефона, город, номер банковской карты
def entry_name(message):
    name = message.text
    bot.send_message(message.chat.id, f"Ваше имя: {name}")
    bot.send_message(message.chat.id, f"Окей, а сколько вам лет?")
    bot.register_next_step_handler(message, entry_age)

def entry_age(message):
    age = message.text
    bot.send_message(message.chat.id, f"Ваш возраст: {age}")
    bot.send_message(message.chat.id, f"Окей, а какой у тебя номер телефона?")
    
    
    

@bot.message_handler(content_type=['text'])
def weather_menu(message):
    city = message.text
    API_URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_TOKEN}'
    r = requests.get(API_URL)
    w = r.json()
    
    bot.send_message(message.chat.id, f"Вы ввели: {city}")
    bot.send_message(message.chat.id, f"Ищем температуру для этого города")
    bot.send_message(message.chat.id,
                     f'''В городе {w['name']}\n
                     температура: {w['main']['temp'] - 273.15}
                     ''')
    
    
    

bot.polling()






