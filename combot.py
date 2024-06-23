import os
import requests
import json
import datetime
import history
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP


class User:
    """Основной класс User"""

    def __init__(self):
        """Инициализация:

        :param self.city = Запрос от пользователя по городу.
        :param self.hostels = Запрос от пользователя по отелям.

        :param self.min_money = Минимальная цена в $
        :param self.max_money = Максимальная цена в $

        :param self.number_hostels = Количество отелей для вывода.
        :param self.need_photo = Требуется ли вывод фотографий (по стандарту 'NO')
        :param self.mode = Модификация вывода для поиска отелей.

        :param self.text = Весь текст содержащий в себе данные о отелях

        :param self.day_in = День въезда
        :param self.month_in = Месяц въезда
        :param self.year_in = Год въезда

        :param self.day_out = День выезда
        :param self.month_out = месяц выезда
        :param self.year_out = Год выезда


        """
        self.user_id = None

        self.city = None
        self.hostels = None

        self.min_money = None
        self.max_money = None
        self.distance = None

        self.number_hostels = None
        self.need_photo = 0
        self.number_photo = None
        self.mode = None
        self.command = None

        self.text = []
        self.text_dict = []

        self.day_in = None
        self.month_in = None
        self.year_in = None

        self.day_out = None
        self.month_out = None
        self.year_out = None

    def set_user_id(self, user_id: str):
        """Сеттер Пользовательского айди
        :param user_id
        :type user_id: str
        """
        self.user_id = user_id

    def set_city(self, city: str):
        """Сеттер города
        :param city
        :type city: str
        """
        self.city = city

    def set_hostels(self, hostels: int):
        """Сеттер отелей
        :param hostels
        :type hostels: list
        """
        self.hostels = hostels

    def set_min_money(self, min_money: int):
        """Сеттер Минимальной цены в $
        :param min_money
        :type min_money: int
        """
        self.min_money = min_money

    def set_max_money(self, max_money: int):
        """Сеттер Максимальной цены в $
        :param max_money
        :type max_money: int
        """
        self.max_money = max_money

    def set_distance(self, distance: int):
        """Сеттер Максимальной цены в $
        :param distance
        :type distance: int
        """
        self.distance = distance

    def set_number_hostels(self, number_hostels: int):
        """Сеттер количества отелей установленным пользователем
        :param number_hostels
        :type number_hostels: int
        """
        self.number_hostels = number_hostels

    def set_need_photo(self, need_photo):
        """Сеттер нужности фотографий при выводе
        :param need_photo
        :type need_photo
        """
        self.need_photo = need_photo

    def set_number_photo(self, number_photo):
        """Сеттер количество фотографий при выводе
        :param number_photo
        :type number_photo
        """
        self.number_photo = number_photo

    def set_mode(self, mode: str):
        """Сеттер Модификации поиска
        :param mode
        :type mode: str
        """
        self.mode = mode

    def set_command(self, command: str):
        """Сеттер команды поиска
        :param command
        :type command: str
        """
        self.command = command

    def set_text_clear(self):
        """Сеттер текста
        :param
        :type
        """
        self.text_dict.clear()

    def set_text_dict(self, text_dict: dict):
        """Сеттер текста
        :param text_dict
        :type text_dict: dict
        """
        # self.text.append(text)
        self.text_dict.append(text_dict)

    def set_datetime_in(self, day, month, year):
        """Сеттер времени въезда в отель
        :param day
        :param month
        :param year
        :type day: int
        :type month: int
        :type year: int
        """
        self.day_in = day
        self.month_in = month
        self.year_in = year

    def set_datetime_out(self, day, month, year):
        """Сеттер времени выезда из отеля
        :param day
        :param month
        :param year
        :type day: int
        :type month: int
        :type year: int
        """
        self.day_out = day
        self.month_out = month
        self.year_out = year

    def get_user_id(self):
        """Геттер Пользовательского айди
        :param self.user_id
        :return self.user_id
        """
        return self.user_id

    def get_city(self):
        """Геттер города
        :param self.city
        :return self.city
        """
        return self.city

    def get_hostels(self):
        """Геттер отелей
        :param self.hostels
        :return self.hostels
        """
        return self.hostels

    def get_max_money(self):
        """Геттер Максимальной цены в $
        :param self.max_money
        :return self.max_money
        """
        if self.max_money == None:
            return 150
        else:
            return self.max_money

    def get_min_money(self):
        """Геттер Минимальной цены в $
        :param self.min_money
        :return self.min_money
        """
        if self.min_money == None:
            return 100
        else:
            return self.min_money

    def get_distance(self):
        """Геттер Дистанции
        :param self.distance
        :return self.distance
        """
        return self.distance

    def get_number_hostels(self):
        """Геттер количества отелей
        :param  self.number_hostels
        :return self.number_hostels
        """
        return self.number_hostels

    def get_need_photo(self):
        """Геттер необходимости фото
        :param  self.need_photo
        :return 'YES' or 'NO'
        """
        if self.need_photo == 1:
            return 'YES'
        else:
            return 'NO'

    def get_number_photo(self):
        """Геттер количества фото
        :param  self.number_photo
        :return self.number_photo
        """
        return self.number_photo
    def get_mode(self):
        """Геттер модификации для поиска
        :param self.mode
        :return self.mode
        """
        return self.mode

    def get_command(self):
        """Геттер ввода команды для поиска
        :param self.command
        :return self.command
        """
        return self.command

    def get_text(self):
        """Геттер текста
        :param self.text
        :return self.text
        """
        return self.text

    def get_text_dict(self):
        """Геттер текста
        :param self.text
        :return self.text
        """
        return self.text_dict

    def get_day_in(self):
        """Геттер дня вьезда
        :param self.day_in
        :return self.day_in
        """
        return self.day_in

    def get_month_in(self):
        """Геттер месяца вьезда
        :param self.month_in
        :return self.month_in
        """
        return self.month_in

    def get_year_in(self):
        """Геттер года вьезда
        :param self.year_in
        :return self.year_in
        """
        return self.year_in

    def get_day_out(self):
        """Геттер дня выезда
        :param self.day_out
        :return self.day_out
        """
        return self.day_out

    def get_month_out(self):
        """Геттер месяца выезда
        :param self.month_out
        :return self.month_out
        """
        return self.month_out

    def get_year_out(self):
        """Геттер года выезда
        :param self.year_out
        :return self.year_out
        """
        return self.year_out

    def get_days_dates(self):
        """Геттер дат, необходим для получения количество дней нахождения в отеле для расчетов стоимости общей суммы
        Условие:Если интовое значение месяца въезда равна(==) интовое значение месяца выезда,
        то суммируем все значения(Год + месяц + день въезда/выезда) и вычитаем из дня выезда день заезда
        :return days
        Условие:Если интовое значение месяца въезда больше(<) интовое значение месяца выезда,
        то суммируем все значения(Год + месяц(умножаем на 30 дней) + день въезда/выезда) и вычитаем из дня выезда день заезда
        :return days
        """
        if int(self.month_in) == int(self.month_out):
            date_in = int(self.year_in) + int(self.month_in) + int(self.day_in)
            date_out = int(self.year_out) + int(self.month_out) + int(self.day_out)
            days = date_out - date_in
            return days
        elif int(self.month_in) < int(self.month_out):
            date_in = int(self.year_in) + (int(self.month_in) * 30) + int(self.day_in)
            date_out = int(self.year_out) + (int(self.month_out) * 30) + int(self.day_out)
            days = date_out - date_in
            return days


class CommandsTelegram:
    """Команды телеграмма, содержит в себе всю логику."""
    print(f'Бот был запущен в', datetime.datetime.now().strftime('Дата: %Y %m %d Время: %H:%M:%S'))

    def __init__(self, bot):
        """Инициализация:
        self.bot = bot из main (TGBOT) содержит в себе обращение к телеграмму
        self.user_data = User() Инициализация Юзера и обращение к нему
        self.history = history.DataBase(user_id=self.user_data) Инициализация Базы Данных

        """
        self.bot = bot
        self.user_data = User()
        self.history = history.DataBase(self.bot)

    def ask_set_city(self, message):
        """Запрос у пользователя Города.
        Отправка сообщение пользователю с вопросом
        Активация Базы данных self.history.create_db()
        Установка города от запроса пользователя в переменной self.user_data.set_city(city=message.text)
        Установка значения запроса от пользователя в переменной self.history.set_request(request=self.user_data.get_city())

        Переход к следующей функции: (ask_number_hostels) Количеству отелей
        :param message:
        :return:
        """
        if message.text == '/help':
            self.Help(message)

        else:
            self.user_data.set_city(city=message.text)
            self.bot.send_message(self.user_data.get_user_id(), 'Количество отелей для поиска: ')
            self.bot.register_next_step_handler(message, self.ask_hostels_number)

    def ask_hostels_number(self, message):
        """Запрос у пользователя о минимальной цене

        :param message:
        :return:
        """
        if message.text == '/help':
            self.Help(message)

        else:
            if isinstance(message.text.isdigit(), int):
                self.user_data.set_number_hostels(number_hostels=int(message.text))
                if self.user_data.get_command() == 'highprice':
                    self.bot.send_message(self.user_data.get_user_id(), 'Введите минимальную цену в $: ')
                    self.bot.register_next_step_handler(message, self.ask_price_min)
                else:
                    self.ask_need_photo()
            else:
                self.bot.send_message(self.user_data.get_user_id(), f'Было введено неверно - "{message.text}" не число.'
                                                                    f' Необходимо цифровое значение ')
                self.bot.register_next_step_handler(message, self.ask_hostels_number)

    def ask_price_min(self, message):
        """Запрос у пользователя о минимальной цене

        :param message:
        :return:
        """
        if message.text == '/help':
            self.Help(message)

        else:
            if isinstance(message.text.isdigit(), int):
                self.user_data.set_min_money(min_money=int(message.text))
                self.bot.send_message(self.user_data.get_user_id(), 'Введите максимальную цену в $: ')
                self.bot.register_next_step_handler(message, self.ask_price_max)

            else:
                self.bot.send_message(self.user_data.get_user_id(), f'Было введено неверно - "{message.text}" не число.'
                                                                    f' Необходимо цифровое значение ')
                self.bot.register_next_step_handler(message, self.ask_price_min)

    def ask_price_max(self, message):
        """Запрос у пользователя о максимальной цене

        :param message:
        :return:
        """
        if message.text == '/help':
            self.Help(message)

        else:
            if isinstance(message.text.isdigit(), int):
                self.user_data.set_max_money(max_money=int(message.text))
                self.bot.send_message(self.user_data.get_user_id(), 'Введите минимальную дистанцию от центра города в км.: ')
                self.bot.register_next_step_handler(message, self.ask_distance_of_midle_city)

            else:
                self.bot.send_message(self.user_data.get_user_id(), f'Было введено неверно - "{message.text}" не число.'
                                                                    f' Необходимо цифровое значение ')
                self.bot.register_next_step_handler(message, self.ask_price_max)

    def ask_distance_of_midle_city(self, message):
        """Запрос у пользователя о дистанции от центра города

        :param message:
        :return:
        """
        if message.text == '/help':
            self.Help(message)

        else:
            if isinstance(message.text.isdigit(), int):
                self.user_data.set_distance(distance=int(message.text))
                self.ask_need_photo()

            else:
                self.bot.send_message(self.user_data.get_user_id(), f'Было введено неверно - "{message.text}" не число.'
                                                                    f' Необходимо цифровое значение ')
                self.bot.register_next_step_handler(message, self.ask_distance_of_midle_city)

    def ask_number_photo(self, message):
        """Запрос у пользователя о количестве фото в сообщении

        :param message:
        :return:
        """
        if message.text == '/help':
            self.Help(message)

        else:
            if isinstance(message.text.isdigit(), int):
                self.user_data.set_number_photo(number_photo=int(message.text))
                self.info_city(message=message)

            else:
                self.bot.send_message(self.user_data.get_user_id(), f'Было введено неверно - "{message.text}" не число.'
                                                                    f' Необходимо цифровое значение ')
                self.bot.register_next_step_handler(message, self.ask_number_photo)

    def ask_need_photo(self):
        """Запрос у пользователя о необходимости фото
        Условие если message == 'Да' или (or) 'да', то установка значения необходимости фото в 1 ('YES')
        Переход к следующей функции (info) запрос у Hostels

        Условие если message != 'Да' или (or) 'да', то установка значения необходимости фото в 0 ('NO')
        Переход к следующей функции (info) запрос у Hostels

        :param
        :return:
        """
        markup_inline = types.InlineKeyboardMarkup()
        markup_inline.add(types.InlineKeyboardButton(text='Да', callback_data='YES'),
                          types.InlineKeyboardButton(text='Нет', callback_data='NO')
                          )

        self.bot.send_message(self.user_data.get_user_id(), os.getenv('b_ask_need_photo'), reply_markup=markup_inline)

    def info_city(self, message):
        """Запросы у Hostels
        Сбор всех значений полученых во время запросов и установка их значений в User
        :param message:
        :return:
        """

        self.bot.send_message(self.user_data.get_user_id(), 'Подождите, данные загружаются...', parse_mode='Markdown')

        "Запрос у Hostels поиск по названию города"

        url = os.getenv('url_search_loc')
        querystring = {"q": self.user_data.get_city(), "locale": "en_US", "langid": "1033",
                       "siteid": "300000001"}
        headers = {
            "X-RapidAPI-Key": os.getenv('RapidAPI_Key'),
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)

        "Запрос у Hostels списка всех отелей в регионе города."
        try:
            url = os.getenv('url_search_list')
            payload = {
                "currency": "USD",
                "eapid": 1,
                "locale": "en_US",
                "siteId": 300000001,
                "destination": {"regionId": data['sr'][0]['gaiaId']},
                "checkInDate": {
                    "day": int(self.user_data.get_day_in()),
                    "month": int(self.user_data.get_month_in()),
                    "year": int(self.user_data.get_year_in())},
                "checkOutDate": {
                    "day": int(self.user_data.get_day_out()),
                    "month": int(self.user_data.get_month_out()),
                    "year": int(self.user_data.get_year_out())},
                "rooms": [{"adults": 2}],
                "resultsStartingIndex": 0,
                "resultsSize": 200,
                "sort": str(self.user_data.get_mode()),
                "filters": {"price": {"max": self.user_data.get_max_money(),
                                      "min": self.user_data.get_min_money()}}
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": os.getenv('RapidAPI_Key'),
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            }
            response = requests.request("POST", url, json=payload, headers=headers)
            data = json.loads(response.text)
        except (IndexError) as ex:
            print(ex)
            self.bot.send_message(self.user_data.get_user_id(), 'Произошла ошибка. Сбрасываю настройки')
            self.Help(message)
        self.user_data.set_text_clear()
        self.info_hostels(data=data)

    def info_hostels(self, data):


        """Инициализация
        text_dist = кортеж данных
        lock_hostel = количество считанных данных о отелях
        """

        lock_hostel = 0

        """
        Разбиение всех полученных данных и отправка их значений в переменной
        Условие: если lock_hostel меньше значения установленное в переменной количество отелей,
        то прибавка к переменной lock_hostel += 1 и сбор информации в переменных

        Условие: если lock_hostel больше значения установленное в переменной количество отелей,
        то пропуск значений
        """

        for hostel in data['data']['propertySearch']['properties']:
            if lock_hostel < self.user_data.get_number_hostels():
                text_dict = dict()
                text_dict['name'] = hostel['name']
                text_dict['hostelId'] = int(hostel['id'])
                text_dict['count'] = hostel['mapMarker']['label']
                text_dict['latitude'] = hostel['mapMarker']['latLong']['latitude']
                text_dict['longtidude'] = hostel['mapMarker']['latLong']['longitude']
                text_dict['dist'] = hostel['destinationInfo']['distanceFromDestination']['value']
                text_dict['dist_text'] = hostel['destinationInfo']['distanceFromDestination']['value']
                lock_hostel += 1
                self.user_data.set_text_dict(text_dict=text_dict)
            else:
                break

        self.bot.send_message(self.user_data.get_user_id(), 'Данные загрузились.', parse_mode='Markdown')
        self.message_hostel()

    def message_hostel(self):
        """
        stop_in_history = переменная счетчик для вноса данных в Базу Данных.
        """
        stop_in_history = 0

        """
        Условие: Если стоит значение 'YES' в переменной Необходимости фото (need_photo),
        то переход к следующей функции Фото в сообщения и отправка сообщения пользователю
        
        Условие: Если стоит значение 'NO' в переменной Необходимости фото (need_photo),
        то проходим по всему тексту в переменной текст (text_dict) и отправка сообщение пользователю
        """
        if self.user_data.get_need_photo() == 'YES':
            for number_hostel in self.user_data.get_text_dict():
                hostelId = number_hostel['hostelId']
                name = number_hostel['name']
                count = number_hostel['count']
                latitude = number_hostel['latitude']
                longtidude = number_hostel['longtidude']
                dist = str(int(number_hostel['dist'] * 1.60934))
                dist_text = str(number_hostel['dist_text'])

                coords = f'https://www.google.ru/maps/search/{longtidude}+{latitude}/@{longtidude},{latitude},14.96z'

                text = f'Название отеля: {name}\n' \
                       f'Стоимость за ночь: {count} | ' \
                       f'за все время: ${int(count[1:4]) * self.user_data.get_days_dates()}\n' \
                       f'Дистанция от города: {dist_text} миль ({dist} в км.)\n' \
                       f'Местоположение: {coords}\n'
                if stop_in_history < 1:
                    stop_in_history += 1
                    self.user_data.set_hostels(hostelId)
                    self.history.set_user_id(user_id=self.user_data.get_user_id())
                    self.history.set_request(request=f'{self.user_data.get_city()} {self.user_data.get_command()}')
                    self.history.set_hostels_id(hostels_id=f'Номер отеля: {hostelId}')
                    self.history.set_hostels_name(hostels_name=
                                                  f'Название отеля: {name}\n'
                                                  f'Стоимость за ночь: {count} | '
                                                  f'за все время: ${int(count[1:4]) * self.user_data.get_days_dates()}\n'
                                                  f'Дистанция от города: {dist_text} миль ({dist} в км.)\n'
                                                  f'Местоположение: {coords}\n')
                    self.history.add_in_base()
                self.user_data.set_hostels(hostelId)
                self.photo_in_message(text)

        else:
            for number_hostel in self.user_data.get_text_dict():
                name = number_hostel['name']
                hostelId = number_hostel['hostelId']
                count = number_hostel['count']
                latitude = number_hostel['latitude']
                longtidude = number_hostel['longtidude']
                dist = str(int(number_hostel['dist'] * 1.60934))
                dist_text = str(number_hostel['dist_text'])

                coords = f'https://www.google.ru/maps/search/{longtidude}+{latitude}/@{longtidude},{latitude},14.96z'

                text = f'Название отеля: {name}\n' \
                       f'Стоимость за ночь: {count} | ' \
                       f'за все время: ${int(count[1:4]) * self.user_data.get_days_dates()}\n' \
                       f'Дистанция от города: {dist_text} миль ({dist} в км.)\n' \
                       f'Местоположение: {coords}\n'

                self.bot.send_message(self.user_data.get_user_id(), text=text,
                                      parse_mode='Markdown')
                if stop_in_history < 1:
                    stop_in_history += 1
                    self.user_data.set_hostels(hostelId)
                    self.history.set_user_id(user_id=self.user_data.get_user_id())
                    self.history.set_request(request=f'{self.user_data.get_city()} {self.user_data.get_command()}')
                    self.history.set_hostels_id(hostels_id=f'Номер отеля: {hostelId}')
                    self.history.set_hostels_name(hostels_name=
                                                  f'Название отеля {name}\n'
                                                  f'Стоимость за ночь {count} | '
                                                  f'за все время ${int(count[1:4]) * self.user_data.get_days_dates()}\n'
                                                  f'Дистанция от города {dist_text} миль ({dist} в км.)\n'
                                                  f'Местоположение {coords}\n')
                    self.history.add_in_base()

    def photo_in_message(self, text):
        """ Функция фотографии в сообщении
        Отправка значение Hostels с id Отеля
        Вывод информации пользователю

        :param text:
        :return:
        """

        "Запрос у Hostels все данные о отеле"

        url = os.getenv('url_search_photo')

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": str(self.user_data.get_hostels())
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": os.getenv('RapidAPI_Key'),
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        data = json.loads(response.text)
        image = []

        "Проход по полученных датах и получение всех ссылок на фото"

        for i in data['data']['propertyInfo']['propertyGallery']['images']:
            image.append(i['image']['url'])

        "Ограничитель number_lock"
        number_lock = 0

        """Проход по всему списку и рандомный выбор фото
        Условие: если количество number_lock меньше stop_number,
        то number_lock += 1 и рандомный выбор фото и отправка пользователю
        
        Условие: если количество number_lock больше stop_number,
        то пропуск
        """

        list_images = []

        for _ in image:
            if number_lock < int(self.user_data.get_number_photo()):
                number_lock += 1
                if _ not in list_images:
                    list_images.append(_)
                else:
                    break
            else:
                break
        """Группировка текста с изображениями в одном сообщении и отправка его пользователю"""
        group_media = [types.InputMediaPhoto(list_images[0], caption=text)]
        group_media += [types.InputMediaPhoto(i_image) for i_image in list_images[0:]]
        self.bot.send_media_group(chat_id=self.user_data.get_user_id(),
                                  media=group_media, disable_notification=True)
        return

    def Help(self, message):
        """Функция Help, принимает все сообщения проходящие через getTextMessages
        Возвращает пользователю сообщения со всеми командами и кнопками.

        :param message:
        :return: message: list
        """

        markup_inline = types.InlineKeyboardMarkup()
        markup_inline.add(types.InlineKeyboardButton(text='Низкая цена', callback_data='lowprice'),
                          types.InlineKeyboardButton(text='Большая цена', callback_data='higprice'),
                          types.InlineKeyboardButton(text='Идеальный выбор', callback_data='bestdeal'),
                          types.InlineKeyboardButton(text='История', callback_data='history')
                          )

        if message.text == "Привет":
            self.bot.send_message(message.from_user.id, os.getenv('b_say_help_commands'))
        elif message.text == "/help":
            self.bot.send_message(message.from_user.id, "Здравствуйте!\n"
                                                        "Снизу Вы найдете все команды Бота", reply_markup=markup_inline)
        else:
            self.bot.send_message(message.from_user.id, os.getenv('b_say_help'))

    def getTextMessages(self, message):
        """Функция получения текстовых сообщений
        Принимает все сообщения и перенаправляет в функцию Help

        :param message:
        :return: message: list
        """
        self.Help(message=message)

    def calendar(self, message):
        """Функция Календарь.
        Принимает сообщение пользователя и активирует билдер календаря из библиотеки TelegramCalendar
        Возвращает функцию календаря с id 0 и local = 'ru'.
        :param message:
        :return: message: list
        """
        calendar, step = DetailedTelegramCalendar(calendar_id=0, locale='ru').build()
        self.bot.send_message(message.chat.id, f"Выберите: {LSTEP[step]}", reply_markup=calendar)

    def calendar2(self, message):
        """Функция Календарь.
        Принимает сообщение пользователя и активирует билдер календаря из библиотеки TelegramCalendar
        Возвращает функцию календаря с id 1 и local = 'ru'.
        :param message:
        :return: message: list
        """
        calendar, step = DetailedTelegramCalendar(calendar_id=1, locale='ru').build()
        self.bot.send_message(message.chat.id, f"Выберите: {LSTEP[step]}", reply_markup=calendar)