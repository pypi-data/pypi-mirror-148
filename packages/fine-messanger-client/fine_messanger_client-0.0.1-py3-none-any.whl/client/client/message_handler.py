import sys
import threading
from PyQt5.QtCore import pyqtSignal, QObject
from client.client.common import handler
from datetime import datetime
from time import sleep
from start_window import UserNameDialog
from warning_window import WarningWindow
from PyQt5.QtWidgets import QApplication
import hashlib
import hmac
import binascii


class MessageHandler(QObject, handler.Handler):
    """Main class handler outputs client messages
    and injects server messages.
    """

    signal_message = pyqtSignal(dict)
    signal_sent_message = pyqtSignal(str)
    signal_get_sent = pyqtSignal(int)
    signal_get_accepted = pyqtSignal(int)

    def __init__(self, database):
        QObject.__init__(self)
        handler.Handler.__init__(self)
        self.database = database
        self.app = QApplication(sys.argv)

    def message_from_server(self):
        """Recipient of messages from the server."""

        while True:
            try:
                self.get_message()
                self.server_message_handler()
            except Exception as e:
                print(e)

    def server_message_handler(self):
        """Message handler coming from the server."""

        if 'OK' in self.message.keys():
            print(self.message['OK'])
        elif self.message['action'] == 'registered':
            self.username = self.message['user']
            print(f'The user: {self.message["user"]} registered')
            return True
        elif self.message['action'] == 'refuse':
            self.username = 'Guest'
            print(self.message['response'])
        elif self.message['action'] is None:
            self.username = 'Guest'
            print(self.message['response'])
        elif self.message['action'] == 'wrong_password':
            self.username = 'Guest'
            print(self.message['response'])
            return False
        elif self.message['action'] == 'success':
            self.username = self.message['user']
            print(self.message['response'])
            return True
        elif self.message['action'] == 'message':
            print(f"You've got message from user: {self.message['user']}")
            self.signal_get_accepted.emit(self.message['count'])
            self.signal_message.emit(self.message)
        elif self.message['action'] == 'sent_message':
            print(f'The message was sent to user: {self.message["addressee"]}')
            self.signal_sent_message.emit(self.message["addressee"])
            self.signal_get_sent.emit(self.message['count'])
        elif self.message['action'] == 'got_contact_key':
            print('The key have got from server')
        elif self.message['action'] == 'no_user':
            print(self.message['response'])
        elif self.message['action'] == 'got_contacts':
            print('Contact list have got from server')
        elif self.message['action'] == 'added_contact':
            print(self.message['response'])
        elif self.message['action'] == 'got_all_users':
            print(self.message['response'])
            with threading.Lock():
                self.database.known_users(self.message)

    def set_user(self):
        """User actions: registration, authorisation.
        Launches the initial authorisation window.
        """

        start_window = UserNameDialog()
        self.app.exec_()
        self.username = start_window.client_name.text()
        password = start_window.client_password.text()
        action = start_window.action.lower()

        if self.username:
            with threading.Lock():
                if action == 'authorisation':
                    password_bytes = password.encode('utf-8')
                    solt_bytes = self.username.encode('utf-8')
                    password_hash = hashlib.pbkdf2_hmac('sha256',
                                                        password_bytes,
                                                        solt_bytes, 10000)
                    password_hash_str = binascii.hexlify(password_hash)
                    self.message = {
                        'action': action,
                        'user': self.username
                    }
                    self.send_message()
                    self.get_message()
                    if self.message['response'] == 511:
                        client_hash = hmac.new(password_hash_str,
                                               self.message['data'].encode(
                                                   'utf-8'), 'MD5')
                        digest = client_hash.digest()
                        self.message = {
                            'user': self.username,
                            'data': binascii.b2a_base64(digest).decode(
                                'ascii'),
                            'response': 511
                        }
                        self.send_message()
                        self.get_message()
                        del start_window
                        if self.server_message_handler():
                            return True
                        else:
                            self.set_user()
                    else:
                        print(self.message['response'])
                        del start_window
                        self.set_user()
                elif action == 'registration':
                    self.message = {
                        'action': action,
                        'password': password,
                        'user': self.username
                    }
                    try:
                        self.send_message()
                        self.get_message()
                        if self.server_message_handler():
                            del start_window
                            return True
                    except Exception as e:
                        print(e)

        elif start_window.action == 'exit':
            self.username = 'Guest'
            del start_window
            return False
        else:
            del start_window
            warning = WarningWindow(
                'Incorrect nickname\nDo you want to continue?')
            if warning.message == 'yes':
                del warning
                self.set_user()
            else:
                self.username = 'Guest'
                del warning
                return False

    def update_key(self):
        """The method updates the client key on the server."""

        key = self.database.get_key()
        self.message = {
            'action': 'update_key',
            'user': self.username,
            'key': key.publickey().export_key().decode('ascii')
        }
        with threading.Lock():
            self.send_message()

    def get_contact_key(self, contact):
        """The method requests the contact key from the server."""

        self.message = {
            'action': 'get_contact_key',
            'contact': contact,
            'user': self.username
        }
        with threading.Lock():
            self.send_message()

    def create_massage(self, message, to_user):
        """The method sends a message to the user."""

        message_dict = {
            'action': 'message',
            'user': self.username,
            'addressee': to_user,
            'time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'message': message
        }
        self.message = message_dict
        with threading.Lock():
            self.send_message()
            print(f'The message was sent to user "{to_user}"')

    def get_contacts(self):
        """Get the list of contacts"""

        self.message = {
            'action': 'get_contacts',
            'time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'user': self.username
        }
        with threading.Lock():
            self.send_message()

    def add_contact(self, contact):
        """Add the user to the list of contacts."""

        self.message = {
            'action': 'add_contact',
            'user': self.username,
            'contact': contact
        }
        with threading.Lock():
            self.send_message()

    def del_contact(self, contact):
        """Delete the user from the list of contacts."""

        self.message = {
            'action': 'del_contact',
            'user': self.username,
            'contact': contact
        }
        with threading.Lock():
            self.send_message()

    def known_users(self):
        """Request a list of all users."""

        self.message = {
            'action': 'all_users',
            'user': self.username,
        }
        with threading.Lock():
            self.send_message()

    def create_presence(self):
        """Sending a presence message to the server on login."""

        presence_dict = {
            'action': 'presence',
            'time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'user': self.username
        }
        self.message = presence_dict

    def exit_message(self):
        """Exit message."""

        self.message = {
            'action': 'exit',
            'time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'user': self.username
        }
        try:
            self.send_message()
            sleep(1)
        except Exception as e:
            print(e)
