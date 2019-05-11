from random import randrange

from ..constants import GITHUB_PROJECT_URL, HELP_TEXT, QUOTES, QUOTES_LEN


def get_random_quote(*args):
    return f'🔥{QUOTES[randrange(QUOTES_LEN)]}🔥'


def get_help_text(*args):
    return HELP_TEXT


def get_github_url(*args):
    return GITHUB_PROJECT_URL
