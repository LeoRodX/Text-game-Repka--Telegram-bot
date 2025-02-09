import telebot
from secrets import secrets
from telebot import types


bot = telebot.TeleBot('MY_TOKEN') # Создадим соединение с ботом

# Состояния игры
game_state = {}


# Начало игры
@bot.message_handler(commands=['start'])
def start_game(message):  
    chat_id = message.chat.id
    game_state[chat_id] = {
       'step': 1,
       'characters': ['дедка', 'бабка', 'внучка', 'учка', 'кошка', 'мышка']
    }
    bot.send_message(chat_id, "Вы начали игру 'Репка'!\n"
                                 "Попробуйте вытянуть репку с помощью персонажей.\n"
                                 "Введите имя персонажа, чтобы позвать его на помощь:")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id not in game_state:
        bot.send_message(chat_id, "Начните игру с помощью команды /start")
        return

    user_input = message.text.lower()
    current_state = game_state[chat_id]

    if user_input in current_state['characters']:
        current_state['step'] += 1
        if current_state['step'] > len(current_state['characters']):
            bot.send_message(chat_id, f"Вы позвали {user_input} и вытянули репку! Поздравляем!")
            del game_state[chat_id]
        else:
               bot.send_message(chat_id, f"Вы позвали {user_input}. Кто следующий?")
    else:
        bot.send_message(chat_id, "Такого персонажа нет в игре. Попробуйте еще раз.")

# Запуск бота
bot.polling()
