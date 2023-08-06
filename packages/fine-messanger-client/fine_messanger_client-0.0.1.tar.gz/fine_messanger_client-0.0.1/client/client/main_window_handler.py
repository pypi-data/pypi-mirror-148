import threading
import time
import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QComboBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, Qt

from client_main_window import Ui_MainWindow


class WindowHandler(QMainWindow):
    """Main user window. Contains all the main logic of the client module"""

    def __init__(self, database, handler):
        super().__init__()
        self.handler = handler
        self.database = database
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.tableWidgetUsers.clicked.connect(self.select_active_user)
        self.ui.tableWidgetContacts.clicked.connect(self.select_active_contact)
        self.ui.pushButtonSend.clicked.connect(self.send_message)
        self.ui.pushButtonShowUsers.clicked.connect(self.btn_all_user)
        self.messages = {}
        self.encryptor = None
        self.chat_model = None
        self.active_contact = None
        self.used_contacts_key = {}
        self.key = self.database.get_key()
        self.decrypter = PKCS1_OAEP.new(self.key)
        self.connect_slot()
        self.show()
        self.all_user_list()
        self.get_contact_list()

    def closeEvent(self, event):
        """window close button handler"""

        self.handler.exit_message()

    def get_contact_list(self):
        """Request a list of contacts from the server"""

        self.handler.get_contacts()
        time.sleep(1)
        contacts = self.database.contacts(self.handler.message)
        self.contact_list(contacts)

    def contact_list(self, contacts):
        """Contact list display"""

        rows = len(contacts)
        self.ui.tableWidgetContacts.setRowCount(rows)
        row = 0
        for i in contacts:
            cell_user = QTableWidgetItem(i)
            cell_user.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            combo = QComboBox()
            combo.addItem('Message')
            combo.addItem('Del user')
            self.ui.tableWidgetContacts.setItem(row, 0, cell_user)
            self.ui.tableWidgetContacts.setCellWidget(row, 1, combo)
            row += 1

    def select_active_user(self):
        """Activating a user to send a message, view a message history or
        adding the user to the contact list
        """

        user = self.ui.tableWidgetUsers.currentItem().text()
        row = self.ui.tableWidgetUsers.currentItem().row()
        action = self.ui.tableWidgetUsers.cellWidget(row, 1).currentText()
        if user == self.handler.username:
            print('You can not send the message or add yourself')
            self.ui.pushButtonClear.setDisabled(True)
            self.ui.pushButtonSend.setDisabled(True)
            self.ui.plainTextEdit.setFrameShadow(False)
            return
        else:
            if action == 'Message':
                self.set_active_user(user)
            else:
                self.add_contact(user)

    def select_active_contact(self):
        """Activating the contact to send a message, view a message history or
        delete the user from the contact list
        """

        contact = self.ui.tableWidgetContacts.currentItem().text()
        row = self.ui.tableWidgetContacts.currentItem().row()
        action = self.ui.tableWidgetContacts.cellWidget(row, 1).currentText()
        if action == 'Message':
            self.set_active_user(contact)
        else:
            self.del_contact(contact)

    def set_encryptor(self):
        """The method sets the encryption and activates
        the message record field
        """

        self.encryptor = PKCS1_OAEP.new(
            RSA.import_key(self.used_contacts_key[self.active_contact]))
        self.ui.pushButtonClear.setDisabled(False)
        self.ui.pushButtonSend.setDisabled(False)
        self.ui.plainTextEdit.setFrameShadow(True)
        self.ui.plainTextEdit.setFocus()
        self.chat()

    def set_active_user(self, contact):
        """Sets the active user and requests the user's key from the server"""

        self.active_contact = contact
        if contact not in self.used_contacts_key.keys():
            try:
                self.handler.get_contact_key(contact)
                time.sleep(0.5)
                key = self.handler.message['key']
                if key:
                    self.used_contacts_key[contact] = key
                    self.set_encryptor()
            except Exception as e:
                print(f'error: {e}')
                self.ui.pushButtonClear.setDisabled(True)
                self.ui.pushButtonSend.setDisabled(True)
                self.ui.plainTextEdit.setFrameShadow(False)
                self.encryptor = None
                return
        else:
            self.set_encryptor()

    def del_contact(self, contact):
        """Request to delete a contact"""

        self.handler.del_contact(contact)
        time.sleep(1)
        if self.handler.message['action'] == 'deleted_contact':
            contacts = self.database.contacts(self.handler.message)
            self.contact_list(contacts)

    def add_contact(self, contact):
        """Request to add a contact"""

        self.handler.add_contact(contact)
        time.sleep(1)
        if self.handler.message['action'] == 'added_contact':
            contacts = self.database.contacts(self.handler.message)
            self.contact_list(contacts)

    def all_user_list(self):
        """User list display"""

        with threading.Lock():
            count = self.database.get_count()
            self.ui.lcdNumberAccept_2.display(str(count[0]))
            self.ui.lcdNumberAccept.display(str(count[1]))
            users = self.database.get_users()
            rows = len(users)
            self.ui.tableWidgetUsers.setRowCount(rows)
            row = 0
            for i in users:
                cell_user = QTableWidgetItem(i)
                cell_user.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                combo = QComboBox()
                combo.addItem('Message')
                combo.addItem('Add user')
                self.ui.tableWidgetUsers.setItem(row, 0, cell_user)
                self.ui.tableWidgetUsers.setCellWidget(row, 1, combo)
                row += 1

    def btn_all_user(self):
        """Button to update the list of users"""

        self.handler.known_users()
        time.sleep(0.5)
        self.all_user_list()

    def btn_online_user(self):
        pass

    @pyqtSlot(int)
    def set_sent_lcd(self, count):
        """Setting sent message's display"""

        self.ui.lcdNumberAccept_2.display(str(count))
        self.database.message_counter(count, 'sent')

    @pyqtSlot(int)
    def set_accepted_lcd(self, count):
        """Setting accepted message's display"""

        self.ui.lcdNumberAccept.display(str(count))
        self.database.message_counter(count, '')

    def send_message(self):
        """Encryption and sending messages to the user"""

        message = self.ui.plainTextEdit.toPlainText()
        if not message:
            return
        encrypt_message = self.encryptor.encrypt(message.encode('utf-8'))
        encrypt_message_base64 = base64.b64encode(encrypt_message)
        self.handler.create_massage(encrypt_message_base64.decode('ascii'),
                                    self.active_contact)
        self.messages[self.active_contact] = message
        self.ui.plainTextEdit.clear()

    def chat(self):
        """Application main chat"""

        with threading.Lock():
            message_list = self.database.get_message(self.active_contact)
        if not self.chat_model:
            self.chat_model = QStandardItemModel()
            self.ui.listView.setModel(self.chat_model)
        self.chat_model.clear()
        for i in message_list:
            if i[0] == self.active_contact:
                row = QStandardItem(
                    f'Input message from:'
                    f' {i[0]} {i[3].replace(microsecond=0)}\n{i[2]}')
                row.setEditable(False)
                row.setBackground(QBrush(QColor(255, 213, 213)))
                row.setTextAlignment(Qt.AlignLeft)
                self.chat_model.appendRow(row)
            else:
                row = QStandardItem(
                    f'Message to:'
                    f' {i[1]} {i[3].replace(microsecond=0)}\n{i[2]}')
                row.setEditable(False)
                row.setBackground(QBrush(QColor(204, 255, 204)))
                row.setTextAlignment(Qt.AlignRight)
                self.chat_model.appendRow(row)
        self.ui.listView.scrollToBottom()

    @pyqtSlot(str)
    def sent_message(self, contact):
        """Assert that the message is delivered to the user
        and added to the database history table
        """

        self.database.message_history(self.handler.username, contact,
                                      self.messages[contact])
        self.active_contact = contact
        self.set_active_user(contact)
        del self.messages[contact]

    @pyqtSlot(dict)
    def new_message(self, message):
        """Receiving and decrypting a message from the user,
        saving it to the database history table and showing it in the chat
        """

        contact = message['user']
        text = message['message']
        encrypted_message = base64.b64decode(text)
        try:
            decrypted_message = self.decrypter.decrypt(encrypted_message)
        except Exception as e:
            print(e)
            return
        self.database.message_history(contact, self.handler.username,
                                      decrypted_message.decode('utf-8'))
        self.active_contact = contact
        self.set_active_user(contact)

    def connect_slot(self):
        """Connecting signals and slots between the message handler
        and the main application window
        """

        self.handler.signal_message.connect(self.new_message)
        self.handler.signal_sent_message.connect(self.sent_message)
        self.handler.signal_get_sent.connect(self.set_sent_lcd)
        self.handler.signal_get_accepted.connect(self.set_accepted_lcd)
