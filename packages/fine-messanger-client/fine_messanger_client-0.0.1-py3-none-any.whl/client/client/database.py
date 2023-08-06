import os
from datetime import datetime

from sqlalchemy import create_engine, Table, Column, Integer, String, Text, \
    MetaData, DateTime, ForeignKey
from sqlalchemy.orm import mapper, Session
from sqlalchemy.sql import default_comparator
from Crypto.PublicKey import RSA


class Storage:
    """The class is a wrapper for working with the client's database.
    Uses SQLite database, implemented with
    SQLAlchemy ORM and uses the classic approach.
    """

    class UserInfo:
        def __init__(self, username, key):
            self.id = None
            self.username = username
            self.date_registration = datetime.now()
            self.key = key

    class KnownUsers:
        def __init__(self, username):
            self.id = None
            self.username = username

    class MessageHistory:
        def __init__(self, from_user, to_user, message):
            self.id = None
            self.from_user = from_user
            self.to_user = to_user
            self.message = message
            self.date = datetime.now()

    class Contacts:
        def __init__(self, contact):
            self.id = None
            self.contact = contact

    class MessageCount:
        def __init__(self):
            self.id = None
            self.sent = 0
            self.accepted = 0

    def __call__(self, username):

        self.username = username
        self.metadata = MetaData()
        self.engine = create_engine(f'sqlite:///db/client_{self.username}.db3',
                                    echo=False, pool_recycle=7200,
                                    connect_args={'check_same_thread': False})

        user_info = Table('user_info', self.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('username', String,
                                 ForeignKey('message_count.id')),
                          Column('date_registration', DateTime),
                          Column('key', Text)
                          )

        known_users = Table('known_users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('username', String)
                            )

        message_history = Table('message_history', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('from_user', String),
                                Column('to_user', String),
                                Column('message', Text),
                                Column('date', DateTime)
                                )

        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('contact', String, unique=True)
                         )

        message_count = Table('message_count', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('sent', Integer),
                              Column('accepted', Integer)
                              )

        self.metadata.create_all(self.engine)
        mapper(self.UserInfo, user_info)
        mapper(self.KnownUsers, known_users)
        mapper(self.MessageHistory, message_history)
        mapper(self.Contacts, contacts)
        mapper(self.MessageCount, message_count)
        self.session = Session(bind=self.engine)

    def add_user(self):
        """Adding a new user and generating an encryption key for him"""

        key = RSA.generate(2048, os.urandom).export_key()
        row = self.UserInfo(self.username, key)
        self.session.add(row)
        self.session.commit()
        row = self.MessageCount()
        self.session.add(row)
        self.session.commit()

    def contacts(self, message):
        """Method - handler user's contact list"""

        if message['action'] == 'got_contacts':
            self.session.query(self.Contacts).delete()
            contacts = message['response']
            for i in contacts:
                contact = self.Contacts(i)
                self.session.add(contact)
                self.session.commit()
        elif message['action'] == 'added_contact':
            if not self.session.query(self.Contacts).filter_by(
                    contact=message['contact']).count():
                contact = self.Contacts(message['contact'])
                self.session.add(contact)
                self.session.commit()
        elif message['action'] == 'deleted_contact':
            if self.session.query(self.Contacts).filter_by(
                    contact=message['contact']).count():
                self.session.query(self.Contacts).filter_by(
                    contact=message['contact']).delete()
                self.session.commit()

        return [user[0] for user in
                self.session.query(self.Contacts.contact).all()]

    def known_users(self, message):
        """Adding known users from server's
        database to the client's database.
        """

        users = message['response']
        self.session.query(self.KnownUsers).delete()
        for i in users:
            user = self.KnownUsers(i)
            self.session.add(user)
            self.session.commit()

    def get_users(self):
        """Getting all known users"""

        return [user[0] for user in
                self.session.query(self.KnownUsers.username).all()]

    def message_counter(self, value, event):
        """Messages counter. Updating user's count of message"""

        row = self.session.query(self.MessageCount).first()
        if event == 'sent':
            row.sent = value
            self.session.commit()
        else:
            row.accepted = value
            self.session.commit()

    def get_count(self):
        """Getting count of messages"""

        query = self.session.query(self.MessageCount.sent,
                                   self.MessageCount.accepted)
        return query.all()[0]

    def message_history(self, user, contact, message):
        """Adding messages to the database table of history"""

        message_row = self.MessageHistory(user, contact, message)
        self.session.add(message_row)
        self.session.commit()

    def get_key(self):
        """Getting secret key of user"""

        key = self.session.query(self.UserInfo.key).first()[0]
        return RSA.import_key(key)

    def get_message(self, contact):
        """Getting user's messages from the history table of the database"""

        from_user = [(i.from_user, i.to_user, i.message, i.date) for i in
                     self.session.query(self.MessageHistory).
                     filter_by(from_user=contact).all()]

        to_user = [(i.from_user, i.to_user, i.message, i.date) for i in
                   self.session.query(self.MessageHistory).
                   filter_by(to_user=contact).all()]
        return sorted(from_user + to_user, key=lambda x: x[3])
