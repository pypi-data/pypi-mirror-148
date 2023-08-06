import argparse
import logging
from datetime import datetime

from colorama import Fore


class ArgParser:
    """ Class that specifies arguments that can be passed
            when launching an application """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader',
                                              prog='rss-reader')

        self.set_cli_arg_options()

    def set_cli_arg_options(self):
        """ Set all positional and optional arguments """
        color_choices = {'red': Fore.RED,
                         'green': Fore.GREEN,
                         'blue': Fore.BLUE,
                         'yellow': Fore.YELLOW,
                         'magenta': Fore.MAGENTA,
                         'black': Fore.BLACK,
                         'cyan': Fore.CYAN
                         }

        self.parser.add_argument('source', help='RSS URL', nargs='?')

        self.parser.add_argument('--version', action='version', version='%(prog)s 5.0.4', help='Print version info')

        self.parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')

        self.parser.add_argument('--verbose', action='store_const', dest='loglevel',
                                 const=logging.INFO, help='Outputs verbose status messages')
        self.parser.add_argument('--limit', metavar='', type=int, nargs='?',
                                 help='Limit news topics if this parameter provided')
        self.parser.add_argument('--date', metavar='', nargs='?', type=self.validate_date,
                                 help='Published date of news in format YYYYMMDD')
        self.parser.add_argument('--to-pdf', metavar='', nargs='?', type=str,
                                 help='Directory and file name where pdf file is stored',)
        self.parser.add_argument('--to-html', metavar='', nargs='?', type=str,
                                 help='Directory and file name where html file is stored',)
        self.parser.add_argument('--clear-cache', help='Clears all news from cache', action='store_true')
        self.parser.add_argument('--colorize', help='Prints stdout in a colored mode',
                                 choices=color_choices, nargs='?')

        self.cli_args = self.parser.parse_args()

        color = color_choices.get(self.cli_args.colorize, Fore.WHITE)
        self.cli_args.colorize = color

    @staticmethod
    def validate_date(date):
        try:
            return datetime.strptime(date, '%Y%m%d')
        except ValueError:
            msg = "not a valid date: {0!r}. Type -h for more info".format(date)
            raise argparse.ArgumentTypeError(msg)
