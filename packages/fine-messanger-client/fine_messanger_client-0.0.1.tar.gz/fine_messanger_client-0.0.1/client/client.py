from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import threading
import time

from PyQt5.QtWidgets import QApplication

from common.descripts import CheckIp, CheckPort
from common.parser import Parser
from common.metaclasses import CheckStatus
from client.message_handler import MessageHandler
from client.database import Storage
from client.main_window_handler import WindowHandler


class Client(metaclass=CheckStatus):

    ip_address = CheckIp()
    server_port = CheckPort()
    """Starting client's application"""

    def __init__(self):
        connection = Parser()
        connection.arg_parser()
        self.database = Storage()
        self.ip_address = connection.ip_address
        self.server_port = connection.port
        self.handler = MessageHandler(self.database)

        self.app = QApplication

    def main(self):
        """Connection to the server method"""

        try:
            self.handler.sock = socket(AF_INET, SOCK_STREAM)
            self.handler.sock.connect((self.ip_address, self.server_port))
            self.handler.create_presence()
            self.handler.send_message()
            self.handler.get_message()
            self.handler.server_message_handler()
            print(f'Hi {self.handler.username}')

            with threading.Lock():
                while self.handler.username == 'Guest':
                    if self.handler.set_user():
                        break
                    else:
                        self.handler.exit_message()
                        time.sleep(1)
                        exit()
            print(f'Hi {self.handler.username}')

        except Exception as e:
            print(e)
        else:
            self.database(self.handler.username)
            if self.handler.message['action'] == 'registered':
                self.database.add_user()
            self.handler.update_key()
            time.sleep(0.5)
            receiver = Thread(target=self.handler.message_from_server)
            receiver.daemon = True
            receiver.start()

            main_window = WindowHandler(self.database, self.handler)
            self.app.exec_()

            while True:
                time.sleep(0.5)
                if receiver.is_alive() and main_window.isActiveWindow():
                    continue
                break


if __name__ == '__main__':
    client = Client()
    client.main()
