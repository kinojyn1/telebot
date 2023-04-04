import telebot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('6173031322:AAFoXoNNJbBBaIVLKFFaOZ8fcW5dKpWWoq4')
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Начнём!')
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton('🔎Найти фильм/сериал по КОДУ', callback_data='1'),
                 InlineKeyboardButton('🤔Для чего нужен этот бот?', callback_data='2'))

    bot.send_message(message.chat.id, '🧐Пожалуйста выберите что Вы хотите узнать:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == '1':
        bot.answer_callback_query(call.id, '🔎 Для поиска отправьте КОД фильма/сериала. Пример: 506')
    elif call.data == '2':
        bot.answer_callback_query(call.id, '🫠Что бы найти фильм/сериал по КОДУ')

@bot.message_handler(content_types=["text"])
def info(message):
    if message.text.lower() == '1':
        file = open("./mina.jpeg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, 'Название фильма: «Мина» — военный триллер 2016 года режиссёров Фабио Гуальоне и Фабио Резинаро. Главную роль сыграл Арми Хаммер. Премьера состоялась 6 октября 2016 года в Италии.')
    if message.text.lower() == '2':
        file = open("./kiber.jpeg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, 'Название сериала: «Киберсталкер» 2019 (2 сезона)')
    if message.text.lower() == '3':
        file = open("./gang.jpeg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Гангстер, коп и дьявол» — южнокорейский боевик 2019 года режиссёра и сценариста Ли Вон Тхэ. В фильме снимались Ма Дон Сок, Ким Му Ёль и Ким Сон Гю. Повествование вращается вокруг трёх персонажей: серийного убийцы, гангстера, который чуть не стал жертвой убийцы, и полицейского, который хочет арестовать убийцу.')
    if message.text.lower() == '4':
        file = open("./krasnoeyw.jpeg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Красное уведомление» 2021 г. Боевик/Комедия  1 ч 58 мин')
    if message.text.lower() == '5':
        file = open("./djentelmenu.jpeg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Джентльмены» 2019 г. Криминал/Боевик 1 ч 53 мин')
    if message.text.lower() == '6':
        file = open("./ktotam.jpg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Кто там» 2015 г. Триллер/Ужасы 1 ч 36 мин')
    if message.text.lower() == '7':
        file = open("./tupoi2.jpg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Тупой и ещё тупее 2» 2014 г. Комедия 1 ч 49 мин')
    if message.text.lower() == '8':
        file = open("./soc.jpg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Социальная сеть» 2010 г. Драма/Историческая драма 2 часа')
    if message.text.lower() == '9':
        file = open ("./Operation.jpg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Операция «Фортуна»: Искусство побеждать 2023 г. Боевик/Комедия 1 ч 54 мин')
    if message.text.lower() == '10':
        file = open ("./stream.jpg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Cтрим» 2022 г. (1 сезон)')
    if message.text.lower() == '11':
        file = open ("./zakatat.jpg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Закатать в асфальт» 2018 г. Криминал/Боевик 2 ч 39 мин')
    if message.text.lower() == '12':
        file = open ("./nobody.jpg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Никто» 2021 г. Криминал/Боевик 1 ч 32 мин')
    if message.text.lower() == '13':
        file = open ("./fakultet.jpg", 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, '«Факультет» 1998 г. Фантастика/ужасы')







bot.polling(none_stop=True)