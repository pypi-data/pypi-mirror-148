import argparse
import sys


class Parser:
    """Command line argument parser"""

    ip_address = ''
    port = 7777
    client_name = 'Guest'

    def arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', default=self.port, type=int, nargs='?')
        parser.add_argument('-a', default=self.ip_address, nargs='?')
        parser.add_argument('-n', '--name', default=self.client_name,
                            nargs='?')
        namespace = parser.parse_args(sys.argv[1:])
        self.ip_address = namespace.a
        self.port = namespace.p
        self.client_name = namespace.name
