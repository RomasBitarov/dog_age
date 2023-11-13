import telebot
from telebot import types
from configure import TOKEN

bot = telebot.TeleBot(TOKEN)
s = 'Окей, теперь напиши сколько полных лет собаке?'
rat = 1

def repeat():
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='да', callback_data='yes')
    key_no = types.InlineKeyboardButton(text='нет', callback_data='no')
    keyboard.add(key_yes, key_no)
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('до 9 кг')
    item2 = types.KeyboardButton('от 9 до 22 кг')
    item3 = types.KeyboardButton('от 22 до 45 кг')
    item4 = types.KeyboardButton('свыше 45 кг')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}.\n Я - Друпи, переведу возраст собаки в человеческий.\n'

                                      ' Для начала выбери вес питомца.'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text(message):
    global rat
    if message.text == 'до 9 кг':
        bot.send_message(message.from_user.id, s, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, reg_age)

    elif message.text == 'от 9 до 22 кг':
        rat = 1.1
        bot.send_message(message.from_user.id, s, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, reg_age)

    elif message.text == 'от 22 до 45 кг':
        rat = 1.2
        bot.send_message(message.from_user.id, s, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, reg_age)

    elif message.text == 'свыше 45 кг':
        rat = 1.3
        bot.send_message(message.from_user.id, s, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, reg_age)
    else:
        bot.send_message(message.from_user.id, 'Выбери один из вариантов!')


def reg_age(message):
    if message.text.isdigit():
        if int(message.text) <= 2:
            bot.send_message(message.from_user.id, f'Человеческий возраст твоей собаки - {round((int(message.text) * 10.5) * rat)}.\n'
                                                   f'Узнать возраст еще одной собаки?', reply_markup=repeat())

        else:
            bot.send_message(message.from_user.id, f'Человеческий возраст твоей собаки - {round(((int(message.text) - 2) * 4 + 21) * rat)}.\n'
                                                   f'Узнать возраст еще одной собаки?', reply_markup=repeat())


    else:
        bot.send_message(message.from_user.id, 'Вводи цифры!')
        bot.register_next_step_handler(message, reg_age)




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, 'Нажми на /start')

    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'До свидания!')


bot.polling(none_stop=True)