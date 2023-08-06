import sys

from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import datetime
from sqlalchemy.ext.declarative import declarative_base
sys.path.append('../')
from common.variables import *


Base = declarative_base()
# Класс - база данных сервера.
class ClientDatabase:
    '''
    Класс клиентской базы данных.
    Обеспечивает:
    :ведение и редактирование списка известных пользователей
    :сохранение истории сообщений
    :ведение и редактирование списка личных контактов каждого клиента
    '''

    class KnownUsers(Base):
        '''
        Класс - отображение таблицы известных пользователей.
        '''
        # Создаём таблицу известных пользователей
        __tablename__ = 'known_users'
        id = Column('id', Integer, primary_key=True)
        username = Column('username', String)

        def __init__(self, user):
            self.id = None
            self.username = user

    # Класс - отображение таблицы истории сообщений
    class MessageHistory(Base):
        '''
        Класс - отображение таблицы истории сообщений клиента
        '''
        # Создаём таблицу истории сообщений
        __tablename__ = 'message_history'
        id = Column('id', Integer, primary_key=True)
        from_user = Column('from_user', String)
        to_user = Column('to_user', String)
        message = Column('message', Text)
        date = Column('date', DateTime)

        def __init__(self, from_user, to_user, message):
            self.id = None
            self.from_user = from_user
            self.to_user = to_user
            self.message = message
            self.date = datetime.datetime.now()

    # Класс - отображение списка контактов
    class Contacts(Base):
        '''
        Класс - отображение таблицы контактов клиента
        '''
        __tablename__ = 'contacts'
        id = Column('id', Integer, primary_key=True)
        name = Column('name', String, unique=True)

        def __init__(self, contact):
            self.id = None
            self.name = contact

    # Конструктор класса:
    def __init__(self, name):
        # Создаём движок базы данных, поскольку разрешено несколько клиентов одновременно,
        # каждый должен иметь свою БД.
        # Поскольку клиент мультипоточный, то необходимо отключить проверки на подключения
        # с разных потоков, иначе sqlite3.ProgrammingError
        self.database_engine = create_engine(f'sqlite:///client_{name}.db3',
                                             echo=False,
                                             pool_recycle=7200,
                                             connect_args={'check_same_thread': False})

        # Создаём таблицы
        Base.metadata.create_all(self.database_engine)

        # Создаём сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # Необходимо очистить таблицу контактов, т.к. при запуске они подгружаются с сервера.
        self.session.query(self.Contacts).delete()
        self.session.commit()


    def add_contact(self, contact):
        '''
        Функция добавления контактов
        '''
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def del_contact(self, contact):
        '''
        Функция удаления контакта
        '''
        self.session.query(self.Contacts).filter_by(name=contact).delete()
        self.session.commit()

    # Пользователи получаются только с сервера, поэтому таблица очищается.
    def add_users(self, users_list):
        '''
        Функция добавления известных пользователей.
        '''
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()


    def save_message(self, from_user, to_user, message):
        '''
         Функция сохранения сообщений
        '''
        message_row = self.MessageHistory(from_user, to_user, message)
        self.session.add(message_row)
        self.session.commit()


    def get_contacts(self):
        '''
        Функция возвращает контакты
        '''
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]


    def get_users(self):
        '''
        Функция возвращает список известных пользователей
        '''
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]


    def check_user(self, user):
        '''
        Функция проверяет наличие пользователя в таблице Известных Пользователей
        '''
        if self.session.query(self.KnownUsers).filter_by(username=user).count():
            return True
        else:
            return False

    def check_contact(self, contact):
        '''
        Функция проверяет наличие пользователя в таблице Контактов
        '''
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    def get_history(self, from_who=None, to_who=None):
        '''
        Функция возвращает историю переписки
        '''
        query = self.session.query(self.MessageHistory)
        if from_who:
            query = query.filter_by(from_user=from_who)
        if to_who:
            query = query.filter_by(to_user=to_who)
        return [(history_row.from_user, history_row.to_user, history_row.message, history_row.date)
                for history_row in query.all()]


# отладка
# if __name__ == '__main__':
    # test_db = ClientDatabase('test1')
    # for i in ['test3', 'test4', 'test5']:
    #     test_db.add_contact(i)
    # test_db.add_contact('test4')
    # test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
    # test_db.save_message('test1', 'test2',
    #                      f'Привет! я тестовое сообщение от {datetime.datetime.now()}!')
    # test_db.save_message('test2', 'test1',
    #                      f'Привет! я другое тестовое сообщение от {datetime.datetime.now()}!')
    # print(test_db.get_contacts())
    # print(test_db.get_users())
    # print(test_db.check_user('test1'))
    # print(test_db.check_user('test10'))
    # print(test_db.get_history('test2'))
    # print(test_db.get_history(to_who='test2'))
    # print(test_db.get_history('test3'))
    # test_db.del_contact('test4')
    # print(test_db.get_contacts())