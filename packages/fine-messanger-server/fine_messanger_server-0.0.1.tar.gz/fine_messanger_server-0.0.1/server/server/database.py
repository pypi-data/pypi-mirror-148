import binascii
import datetime
import hashlib

from sqlalchemy import create_engine, Table, Column, Integer, String,\
    MetaData, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapper, Session
from sqlalchemy.sql import default_comparator


class Storage:
    """The class is a wrapper for working with the server's database.
     Uses SQLite database, implemented with
     SQLAlchemy ORM and uses the classic approach.
    """

    class Users:
        """Table class of all users."""

        def __init__(self, username, password):
            self.id = None
            self.username = username
            self.password = password
            self.key = None
            self.registration_date = datetime.datetime.now()

    class Contacts:
        """User's contact table class."""

        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact
            self.add_contact_time = datetime.datetime.now()

    class UserHistory:
        """Login history table class."""

        def __init__(self, username, ip_address, port, login_time=None,
                     logout_time=None):
            self.id = None
            self.username = username
            self.login_time = login_time
            self.logout_time = logout_time
            self.ip_address = ip_address
            self.port = port

    class ActiveUsers:
        """Active user table class."""

        def __init__(self, user, ip_address, port, login_time):
            self.id = None
            self.user = user
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time

    class MessageHistory:
        """Message history table class."""

        def __init__(self, sender, recipient, sent_message, accepted_message):
            self.id = None
            self.sender = sender
            self.recipient = recipient
            self.sent_message = sent_message
            self.accepted_message = accepted_message
            self.data = datetime.datetime.now()

    class MessageCount:
        """Message counter table class."""

        def __init__(self, username):
            self.id = None
            self.username = username
            self.sent = 0
            self.accepted = 0

    def __init__(self):
        self.engine = create_engine('sqlite:///db/server_base.db3', echo=False,
                                    pool_recycle=7200,
                                    connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        users = Table('Users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String, unique=True),
                      Column('password', String),
                      Column('key', Text),
                      Column('registration_date', DateTime)
                      )

        contacts = Table('Contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('user', ForeignKey('Users.id')),
                         Column('contact', ForeignKey('Users.id')),
                         Column('add_contact_time', DateTime)
                         )

        user_history = Table('User_history', self.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('username', ForeignKey('Users.id')),
                             Column('login_time', DateTime),
                             Column('logout_time', DateTime),
                             Column('ip_address', String),
                             Column('port', Integer)
                             )

        active_users = Table('Active_users', self.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('user', ForeignKey('Users.id')),
                             Column('ip_address', String),
                             Column('port', Integer),
                             Column('login_time', DateTime)
                             )

        message_history = Table('Message_history', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('sender', ForeignKey('Users.id')),
                                Column('recipient', ForeignKey('Users.id')),
                                Column('sent_message', String),
                                Column('accepted_message', String),
                                Column('data', DateTime)
                                )

        message_count = Table('Message_count', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('username', String,
                                     ForeignKey('Users.id')),
                              Column('sent', Integer),
                              Column('accepted', Integer)
                              )

        self.metadata.create_all(self.engine)

        mapper(self.Users, users)
        mapper(self.Contacts, contacts)
        mapper(self.UserHistory, user_history)
        mapper(self.ActiveUsers, active_users)
        mapper(self.MessageHistory, message_history)
        mapper(self.MessageCount, message_count)

        self.session = Session(bind=self.engine)
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def check_username(self, username):
        """Database user check."""

        if self.session.query(self.Users).filter_by(username=username).count():
            return False
        else:
            return True

    def get_password(self, username):
        """Get user password."""

        password = self.session.query(self.Users.password).filter_by(
            username=username)
        return password.one()[0]

    def create_user(self, username, password):
        """Creating a new user and entering into the database"""

        if self.check_username(username):
            password_bytes = password.encode('utf-8')
            solt_bytes = username.encode('utf-8')
            password_hash = hashlib.pbkdf2_hmac('sha256', password_bytes,
                                                solt_bytes, 10000)
            new_user = self.Users(username, binascii.hexlify(password_hash))
            self.session.add(new_user)
            self.session.commit()
            new_user_in_message_count = self.MessageCount(username)
            self.session.add(new_user_in_message_count)
            self.session.commit()
            return True
        else:
            return False

    def add_active_users(self, username, ipaddress, port):
        """Adding an active user to the database table"""

        user = self.ActiveUsers(username, ipaddress, port,
                                login_time=datetime.datetime.now())
        self.session.add(user)
        self.session.commit()

    def update_key(self, username, key):
        """Update user's key"""

        user_key = self.session.query(self.Users).filter_by(
            username=username).first()
        if user_key.key != key:
            user_key.key = key

    def remove_active_users(self, username):
        """Removing an outgoing user"""

        self.session.query(self.ActiveUsers).filter_by(user=username).delete()
        self.session.commit()

    def user_history(self, username, ip_address, port, status):
        """Adding user inputs and outputs to the database table"""

        if status == 'login':
            history = self.UserHistory(username, ip_address, port,
                                       login_time=datetime.datetime.now())
            self.session.add(history)
            self.session.commit()
        else:
            user = self.session.query(self.UserHistory).filter_by(
                username=username, logout_time=None) \
                .order_by(self.UserHistory.id.desc()).first()
            setattr(user, 'logout_time', datetime.datetime.now())
            self.session.commit()

    def get_key(self, username):
        """Getting a user key"""

        key = self.session.query(self.Users).filter_by(
            username=username).first()
        return key.key

    def get_contacts(self, username):
        """Getting a user's contact list"""

        return [user[0] for user in
                self.session.query(self.Contacts.contact).filter_by(
                    user=username).all()]

    def add_contact(self, user, contact):
        """Adding a user to the selected user's contact list"""

        if self.check_username(contact) is False:
            if self.session.query(self.Contacts).filter_by(user=user,
                                                           contact=contact).\
                                                                    count():
                return False
            else:
                add_contact = self.Contacts(user, contact)
                self.session.add(add_contact)
                self.session.commit()
                return True
        else:
            return 'no_contact'

    def del_contact(self, user, contact):
        """Removing a user from the selected user's contact list"""

        if self.check_username(contact) is False:
            if self.session.query(self.Contacts).filter_by(user=user,
                                                           contact=contact).\
                                                                    count():
                self.session.query(self.Contacts).filter_by(user=user,
                                                            contact=contact).\
                                                                    delete()
                self.session.commit()
                return True
            else:
                return 'no_contact'
        else:
            return False

    def active_users_list(self):
        """Getting a list of active users"""

        query = self.session.query(
            self.ActiveUsers.user,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        )
        return query.all()

    def get_all_users(self):
        """Getting all known users"""

        return [user[0] for user in
                self.session.query(self.Users.username).all()]

    def message_count(self, username):
        """Get the number of messages of the selected user"""

        query = self.session.query(
            self.MessageCount.sent,
            self.MessageCount.accepted
        ).filter_by(username=username).all()
        return query[0]

    def add_message_history(self, sender, recipient, message, action):
        """Adding message history to the database table of the selected user"""

        if action == 'sent':
            row = self.MessageHistory(sender, recipient, message,
                                      accepted_message=None)
            self.session.add(row)
            sender_row = self.session.query(self.MessageCount).filter_by(
                username=sender).first()
            sender_row.sent += 1
            self.session.commit()
        else:
            row = self.MessageHistory(sender, recipient, sent_message=None,
                                      accepted_message=message)
            self.session.add(row)
            recipient_row = self.session.query(self.MessageCount).filter_by(
                username=recipient).first()
            recipient_row.accepted += 1
            self.session.commit()


if __name__ == '__main__':
    test = Storage()
    test.message_count('qqq')
