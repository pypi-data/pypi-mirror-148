from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, \
    QLabel, qApp


class UserNameDialog(QDialog):
    """The user's start window asks for a username and password
    to log into the main application
    """

    def __init__(self):
        super().__init__()
        self.action = ''

        self.setWindowTitle('Hello guest')
        self.setFixedSize(275, 120)

        self.label = QLabel('Nickname:', self)
        self.label.move(10, 20)
        self.label.setFixedSize(150, 10)

        self.label = QLabel('Password:', self)
        self.label.move(10, 50)
        self.label.setFixedSize(150, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setMaxLength(30)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(100, 20)

        self.client_password = QLineEdit(self)
        self.client_password.setEchoMode(QLineEdit.Password)
        self.client_password.setMaxLength(50)
        self.client_password.setFixedSize(154, 20)
        self.client_password.move(100, 50)

        self.btn_auth = QPushButton('Authorisation', self)
        self.btn_auth.move(150, 90)
        self.btn_auth.clicked.connect(self.auth_handler)

        self.btn_reg = QPushButton('Registration', self)
        self.btn_reg.move(50, 90)
        self.btn_reg.clicked.connect(self.reg_handler)

        self.show()

    def closeEvent(self, event):
        """Close window handler"""

        self.action = 'exit'

    def auth_handler(self):
        """Authorization handler"""

        if self.client_name.text() and self.client_password.text():
            self.action = self.btn_auth.text()
            qApp.exit()

    def reg_handler(self):
        """Registration handler"""

        if self.client_name.text() and self.client_password.text():
            self.action = self.btn_reg.text()
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = UserNameDialog()
    app.exec_()
