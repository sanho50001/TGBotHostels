import sqlite3
import datetime


class DataBase:
    """Базовая модель Базы Данных"""
    def __init__(self, bot):
        """Инициализация Базы Данных.

        :param self.User_id = Юзер Айди
        :param self.request = Запрос пользователя (Город)
        :param self.datetime = datetime.datetime.now().strftime('Дата: %Y %m %d Время: %H:%M:%S')
        :param self.hostels_id = Айди Отеля
        :param self.hostels_name = Полная информация о отеле
        :param self.bot = Инициализация Бота, команды отправляются туда.
        """
        self.User_id = None
        self.request = ''
        self.datetime = datetime.datetime.now().strftime('Дата: %Y %m %d Время: %H:%M:%S')
        self.hostels_id = ''
        self.hostels_name = ''
        self.bot = bot

    def create_db(self):
        """Создание Базы Данных выше директории пользователя
        С помощью контекстого менеджера with создается база данных и подключается к ней,
        после идет инициализация курсора Базы Данных.

        Создается База данных с:
                user_id TEXT,
                requests TEXT,
                datatime TEXT,
                hostels_id int,
                hostels_name TEXT

        после подтверждение внесение в базу данных.
        (закрытие соединения не требуется, контекстный менеджер сам закрывает соединение)
        """

        with sqlite3.connect('../TelegramDB.db') as db:
            sql = db.cursor()

            sql.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id TEXT,
                requests TEXT,
                datatime TEXT,
                hostels_id int,
                hostels_name TEXT
                )""")
            db.commit()
            return print('База Данных была обновленна.')

    def add_in_base(self):
        """Добавление в Базу Данных.
        С помощью контекстого менеджера with создается база данных(если есть, то только подключение) и подключается к ней,
        после идет инициализация курсора Базы Данных.
        Внесение данных:
                self.User_id = self.User_id
                self.request = self.request
                self.datetime = self.datetime
                self.hostels_id = self.hostels_id
                self.hostels_name = self.hostels_name

        после подтверждение внесение в базу данных.
        (закрытие соединения не требуется, контекстный менеджер сам закрывает соединение)
        """
        with sqlite3.connect('../TelegramDB.db') as db:
            sql = db.cursor()

            sql.execute('INSERT INTO users VALUES (?,?,?,?,?);',
                        (self.User_id, self.request, self.datetime, self.hostels_id, self.hostels_name))
            db.commit()

    def read_in_base(self):
        """Добавление в Базу Данных.
        С помощью контекстого менеджера with создается база данных(если есть, то только подключение) и подключается к ней,
        после идет инициализация курсора Базы Данных.

        Стандартный ограничитель для вывода данных, выше него данные не будут отображаться
        number_lock = 5

        Количество выведенных данных, изначально в 0
        numbers = 0

        Чтение данных:
                self.User_id = user_id = user[0]
                self.request = request = user[1]
                self.datetime = datetimed = user[2]
                self.hostels_id = hostels_id = user[3]
                self.hostels_name = hostels_name = user[4]

        после соединение в переменной text и отправка пользователю.
        (закрытие соединения не требуется, контекстный менеджер сам закрывает соединение)
        """
        with sqlite3.connect('../TelegramDB.db') as db:
            sql = db.cursor()

            number_lock = 5
            numbers = 0

            for user in sql.execute('SELECT * FROM users').fetchall():
                if numbers < number_lock:
                    numbers += 1
                    user_id = user[0]
                    request = user[1]
                    datetimed = user[2]
                    hostels_id = user[3]
                    hostels_name = user[4]
                    text = f'Ваш айди: {user_id}\n' \
                           f'Ваш запрос: {request}\n' \
                           f'Время запроса: {datetimed}\n' \
                           f'Номер отеля в базе данных: {hostels_id}\n' \
                           f'Подробности о отеле: {hostels_name}'
                    self.bot.send_message(self.User_id, text, parse_mode='html')
                else:
                    break

    def delete_db(self, user_id):
        """Удаленние из базы данных.
        С помощью контекстого менеджера with создается база данных(если есть, то только подключение) и подключается к ней,
        после идет инициализация курсора Базы Данных.

        Выбор из Базы данных пользователя с айди user_id и удаление его из Базы Данных,
        после подтверждение внесение изменения в Базу Данных.
        (закрытие соединения не требуется, контекстный менеджер сам закрывает соединение)
        """
        with sqlite3.connect('../TelegramDB.db') as db:
            sql = db.cursor()
            sql.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")
            db.commit()

    def predel(self):
        """Удаленние из базы данных.
        С помощью контекстого менеджера with создается база данных(если есть, то только подключение) и подключается к ней,
        после идет инициализация курсора Базы Данных.

        Выбор из Базы Данных всех позиций и удаление из Базы данных,
        после подтверждение внесение изменения в Базу Данных.
        (закрытие соединения не требуется, контекстный менеджер сам закрывает соединение)
        """
        with sqlite3.connect('../TelegramDB.db') as db:
            sql = db.cursor()
            for _ in sql.execute('SELECT * FROM users'):
                self.delete_db(user_id=_[0])

    def set_user_id(self, user_id):
        """Сеттер user_id
        Принимает user_id и присваивает self.User_id = user_id
        :param user_id
        """
        self.User_id = user_id

    def set_request(self, request):
        """Сеттер user_id
        Принимает user_id и присваивает self.request = request
        :param request
        """
        self.request = request

    def set_hostels_id(self, hostels_id):
        """Сеттер hostels_id
        Принимает hostels_id и присваивает self.hostels_id = hostels_id
        :param hostels_id
        """
        self.hostels_id = hostels_id

    def set_hostels_name(self, hostels_name):
        """Сеттер hostels_id
        Принимает hostels_id и присваивает self.hostels_name = hostels_name
        :param hostels_name
        """
        self.hostels_name = hostels_name

    def get_user_id(self):
        return self.User_id

