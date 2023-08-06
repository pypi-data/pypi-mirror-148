import subprocess
from time import sleep
# from pyfiglet import Figlet
import sys


class Launcher:
    process = []
    act = ''

    def action(self):
        # preview_text = Figlet(font='slant')
        # print(preview_text.renderText('MESSENGER'))
        self.act = input(
            'Please select an action: \n q - exit \n s - start app \n or '
            'any button to close all windows and start again\n')
        if self.act.lower() == 's':
            self.process.append(subprocess.Popen([sys.executable, 'server.py'],
                                                 creationflags=subprocess.
                                                 CREATE_NEW_CONSOLE))
            sleep(1)
            for _ in range(0, 2):
                sleep(0.5)
                self.process.append(
                    subprocess.Popen([sys.executable, 'client.py'],
                                     creationflags=subprocess.
                                     CREATE_NEW_CONSOLE))
            self.action()
        elif self.act.lower() == 'q':
            while self.process:
                self.process.pop().kill()
            sys.exit()
        else:
            while self.process:
                self.process.pop().kill()
            self.action()


launch = Launcher()
launch.action()
