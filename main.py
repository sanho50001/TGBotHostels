import datetime
import combot
import telebot
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(token=os.getenv('TGBot_token'))

TGBOT = combot.CommandsTelegram(bot)


@bot.message_handler(commands=["lowprice"])
def lowprice(message):
    """Функция lowprice, под декоратором message_handler. Вызывается с помощью команды /lowprice
    Принимает сообщение /lowprice и отравлявляет в функцию установку значения города.
    Отправляет значения Модификатора поиска в user_data.set_mode значение ('RECOMMENDED')

    :param message:
    :return:
    """
    try:
        if TGBOT.user_data.get_day_in() == None:
            bot.send_message(message.chat.id, 'Вы не воспользовались календарем для выбора даты заезда/выезда.\n'
                                              'Для того, чтобы продолжить введите команду /calendar')
        else:
            TGBOT.history.create_db()

            TGBOT.user_data.set_mode('RECOMMENDED')
            TGBOT.user_data.set_command('lowprice')
            TGBOT.user_data.set_user_id(message.chat.id)
            bot.send_message(message.chat.id, os.getenv('b_ask_city'))

            bot.register_next_step_handler(message, TGBOT.ask_set_city)
    except AttributeError as ex:
        print(ex)
        bot.register_next_step_handler(message, TGBOT.Help)


@bot.message_handler(commands=["highprice"])
def highprice(message):
    """Функция highprice, под декоратором message_handler. Вызывается с помощью команды /highprice
    Принимает сообщение /highprice и отравлявляет в функцию установку значения города.
    Отправляет значения Модификатора поиска в user_data.set_mode значение ('PRICE_LOW_TO_HIGH')

    :param message:
    :return:
    """
    try:
        if TGBOT.user_data.get_day_in() == None:
            bot.send_message(message.chat.id, 'Вы не воспользовались календарем для выбора даты заезда/выезда.\n'
                                              'Для того, чтобы продолжить введите команду /calendar')
        else:
            TGBOT.history.create_db()
            TGBOT.user_data.set_command('highprice')
            TGBOT.user_data.set_mode('PRICE_LOW_TO_HIGH')
            TGBOT.user_data.set_user_id(message.chat.id)
            bot.send_message(message.chat.id, os.getenv('b_ask_city'))

            bot.register_next_step_handler(message, TGBOT.ask_set_city)
    except AttributeError as ex:
        print(ex)
        bot.register_next_step_handler(message, TGBOT.Help)


@bot.message_handler(commands=["bestdeal"])
def bestdeal(message):
    """Функция bestdeal, под декоратором message_handler. Вызывается с помощью команды /bestdeal
    Принимает сообщение /bestdeal и отравлявляет в функцию установку значения города.
    Отправляет значения Модификатора поиска в user_data.set_mode значение ('RECOMMENDED')

    :param message:
    :return:
    """
    try:
        if TGBOT.user_data.get_day_in() == None:
            bot.send_message(message.chat.id, 'Вы не воспользовались календарем для выбора даты заезда/выезда.\n'
                                              'Для того, чтобы продолжить введите команду /calendar')
        else:
            TGBOT.history.create_db()
            TGBOT.user_data.set_command('bestdeal')
            TGBOT.user_data.set_mode('RECOMMENDED')
            TGBOT.user_data.set_user_id(message.chat.id)
            bot.send_message(message.chat.id, os.getenv('b_ask_city'))

            bot.register_next_step_handler(message, TGBOT.ask_set_city)
    except AttributeError as ex:
        print(ex)
        bot.register_next_step_handler(message, TGBOT.Help)


@bot.message_handler(commands=["history"])
def history(message):
    """Функция history, под декоратором message_handler. Вызывается с помощью команды /history
    Принимает сообщение /history и вызывает поиск по Базе Данных и выводит информацию из Базы данных.

    :param message:
    :return:
    """
    if TGBOT.history.get_user_id() == None:
        TGBOT.history.set_user_id(TGBOT.user_data.get_user_id())
        TGBOT.history.read_in_base()

    else:
        TGBOT.history.read_in_base()


@bot.message_handler(commands=['calendar'])
def start_calendar(message):
    """Функция start_calendar, под декоратором message_handler. Вызывается с помощью команды /calendar
    Принимает сообщение /calendar и запускает билдер календаря

    :param message:
    :return:
    """
    combot.CommandsTelegram.calendar(TGBOT, message)


@bot.callback_query_handler(func=combot.DetailedTelegramCalendar.func(calendar_id=0))
def cal(calendar):
    """Функция start_calendar, под декоратором message_handler. Вызывается с помощью команды /calendar
    Принимает сообщение /calendar и запускает билдер календаря

    :param calendar:
    :return:
    """
    today_date = datetime.date.today()
    result, key, step = combot.DetailedTelegramCalendar(calendar_id=0,
                                                        min_date=today_date,
                                                        locale='ru').process(calendar.data)
    if not result and key:
        bot.edit_message_text(f"Выберите: {combot.LSTEP[step]}",
                              calendar.message.chat.id,
                              calendar.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали: {result}",
                              calendar.message.chat.id,
                              calendar.message.message_id)
        data = []
        i_date = []
        for i in calendar.data.split('_'):
            data.append(i)
        for i_data in data:
            i_date.append(i_data)
        del i_date[0:4]

        year = i_date[0]
        mouth = i_date[1]
        day = i_date[2]
        TGBOT.user_data.set_datetime_in(day, mouth, year)

        TGBOT.calendar2(message=calendar.message)


@bot.callback_query_handler(func=combot.DetailedTelegramCalendar.func(calendar_id=1))
def cal2(calendar):
    """Функция start_calendar, под декоратором message_handler. Вызывается с помощью команды /calendar
    Принимает сообщение /calendar и запускает билдер календаря

    :param calendar:
    :return:
    """

    today_date = datetime.date.today()
    result, key, step = combot.DetailedTelegramCalendar(calendar_id=1,
                                                        min_date=today_date,
                                                        locale='ru').process(calendar.data)
    if not result and key:
        bot.edit_message_text(f"Выберите: {combot.LSTEP[step]}",
                              calendar.message.chat.id,
                              calendar.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали: {result}",
                              calendar.message.chat.id,
                              calendar.message.message_id)
        data = []
        i_date = []
        for i in calendar.data.split('_'):
            data.append(i)
        for i_data in data:
            i_date.append(i_data)
        del i_date[0:4]

        year = i_date[0]
        mouth = i_date[1]
        day = i_date[2]
        TGBOT.user_data.set_datetime_out(day, mouth, year)

        markup_inline = combot.types.InlineKeyboardMarkup()
        markup_inline.add(combot.types.InlineKeyboardButton(text='Низкая цена', callback_data='lowprice'),
                          combot.types.InlineKeyboardButton(text='Большая цена', callback_data='highprice'),
                          combot.types.InlineKeyboardButton(text='Идеальный выбор', callback_data='bestdeal'),
                          combot.types.InlineKeyboardButton(text='История', callback_data='history')
                          )

        bot.send_message(calendar.from_user.id, "Снизу Вы найдете все команды Бота", reply_markup=markup_inline)


@bot.message_handler(commands=['start'])
def start(message):
    """Функция start, под декоратором message_handler. Вызывается с помощью команды /start
    Принимает сообщение /start и запускает билдер календаря

    :param message:
    :return:
    """

    TGBOT.history.create_db()
    b_say = os.getenv('b_start_say')
    markup_inline = combot.types.InlineKeyboardMarkup()
    markup_inline.add(combot.types.InlineKeyboardButton(text='Низкая цена', callback_data='lowprice'),
                      combot.types.InlineKeyboardButton(text='Большая цена', callback_data='highprice'),
                      combot.types.InlineKeyboardButton(text='Идеальный выбор', callback_data='bestdeal'),
                      combot.types.InlineKeyboardButton(text='История', callback_data='history')
                      )
    bot.send_message(message.from_user.id,
                     text=f'{b_say}\n'
                          f'Снизу Вы найдете все команды Бота\n'
                          f'Мини-гайд по использованию бота:\n'
                          f'1 - пропишите команду /calendar для выбора даты, иначе бот не будет работать\n'
                          f'2 - Используйте кнопки чтобы перейти к выбору отеля.',
                     reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    """Функция callback_data перехвата всех вызовов которые возникают при нажатии inline кнопок
    Принимает все вызовы перехватом и проходит по условию, если условие сошлось - переходит дальше по фукнциям
    :param call:
    :return: call
    """

    """'{'id': '2561342649459947012',
     'from_user': {'id': 596359057, 'is_bot': False, 'first_name': 'Александр', 'username': 'Shuero',
                   'last_name': 'Shuero', 'language_code': 'ru', 'can_join_groups': None,
                   'can_read_all_group_messages': None, 'supports_inline_queries': None, 'is_premium': None,
                   'added_to_attachment_menu': None},
     'message': {'content_type': 'text', 'id': 6787, 'message_id': 6787, 'from_user': < telebot.types.User object at
     0x000001F8A93AA910 >, 'date': 1692286186, 'chat': < telebot.types.Chat
    object
    at
    0x000001F8A938BF50 >, 'sender_chat': None, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_sender_name': None, 'forward_date': None, 'is_automatic_forward': None, 'reply_to_message': None, 'via_bot': None, 'edit_date': None, 'has_protected_content': None, 'media_group_id': None, 'author_signature': None, 'text': 'Commands', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'reply_markup': < telebot.types.InlineKeyboardMarkup
    object
    at
    0x000001F8A93B86D0 >, 'message_thread_id': None, 'is_topic_message': None, 'forum_topic_created': None, 'forum_topic_closed': None, 'forum_topic_reopened': None, 'has_media_spoiler': None, 'forum_topic_edited': None, 'general_forum_topic_hidden': None, 'general_forum_topic_unhidden': None, 'write_access_allowed': None, 'user_shared': None, 'chat_shared': None, 'json': {
        'message_id': 6787,
        'from': {'id': 5824374073, 'is_bot': True, 'first_name': 'ShieroBot', 'username': 'TGShieroBot'},
        'chat': {'id': 596359057, 'first_name': 'Александр', 'last_name': 'Shuero', 'username': 'Shuero',
                 'type': 'private'}, 'date': 1692286186, 'text': 'Commands', 'reply_markup': {'inline_keyboard': [
            [{'text': 'start game', 'callback_data': 'startgame'},
             {'text': 'register hero', 'callback_data': 'reghero'}, {'text': 'settings',
                                                                     'callback_data': 'settings'}]]}}}, 'inline_message_id': None, 'chat_instance': '6501844360667391449', 'data': 'settings', 'game_short_name': None, 'json': {
        'id': '2561342649459947012',
        'from': {'id': 596359057, 'is_bot': False, 'first_name': 'Александр', 'last_name': 'Shuero',
                 'username': 'Shuero', 'language_code': 'ru'}, 'message': {'message_id': 6787,
                                                                           'from': {'id': 5824374073, 'is_bot': True,
                                                                                    'first_name': 'ShieroBot',
                                                                                    'username': 'TGShieroBot'},
                                                                           'chat': {'id': 596359057,
                                                                                    'first_name': 'Александр',
                                                                                    'last_name': 'Shuero',
                                                                                    'username': 'Shuero',
                                                                                    'type': 'private'},
                                                                           'date': 1692286186, 'text': 'Commands',
                                                                           'reply_markup': {'inline_keyboard': [[{
                                                                                                                     'text': 'start game',
                                                                                                                     'callback_data': 'startgame'},
                                                                                                                 {
                                                                                                                     'text': 'register hero',
                                                                                                                     'callback_data': 'reghero'},
                                                                                                                 {
                                                                                                                     'text': 'settings',
                                                                                                                     'callback_data': 'settings'}]]}},
        'chat_instance': '6501844360667391449', 'data': 'settings'}}'"""




    if call.data == 'YES':
        TGBOT.user_data.set_need_photo(1)
        bot.send_message(TGBOT.user_data.get_user_id(), 'Сколько фото выводить?')
        bot.register_next_step_handler(call.message, TGBOT.ask_number_photo)
        # TGBOT.ask_number_photo(call.message.chat)

    elif call.data == 'NO':
        TGBOT.user_data.set_need_photo(0)
        TGBOT.info_city(call.message)

    elif call.data == 'lowprice':
        lowprice(call.message)

    elif call.data == 'highprice':
        highprice(call.message)

    elif call.data == 'bestdeal':
        bestdeal(call.message)

    elif call.data == 'history':
        history(call.message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Функция get_text_messages, под декоратором message_handler. Вызывается с помощью любого текста
    Принимает любое сообщение и запускает функцию getTextMessages которая перенаправляет в Help

    :param message:
    :return:
    """
    TGBOT.getTextMessages(message=message)


"""Бот-пуллинг, необходим для полноценной работы. Постоянно обновляется."""

bot.polling(none_stop=True, interval=0)
print(f'Бот завершил работу в', datetime.datetime.now().strftime('Дата: %Y %m %d Время: %H:%M:%S'))



