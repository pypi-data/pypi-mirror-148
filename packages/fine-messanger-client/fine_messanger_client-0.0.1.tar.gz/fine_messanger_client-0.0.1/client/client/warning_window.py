from PyQt5.QtWidgets import QApplication, qApp, QMessageBox
import sys


class WarningWindow(QMessageBox):
    """Warning for incorrect username entry"""

    def __init__(self, message):
        super(WarningWindow, self).__init__()
        self.message = message
        button = self.warning(self, 'Warning', message,
                              buttons=self.Close | self.Apply)
        if button == self.Apply:
            self.message = 'yes'
        else:
            self.message = 'no'
        qApp.quit()


if __name__ == '__main__':
    app = QApplication([])
    start = WarningWindow('Attention')
    sys.exit(app.exec_())
