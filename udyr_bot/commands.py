from logging import getLogger
from random import randrange

from .constants import GITHUB_PROJECT_URL, HELP_TEXT, QUOTES, QUOTES_LEN

log = getLogger(__name__)


def get_random_quote():
    return f'🔥{QUOTES[randrange(QUOTES_LEN)]}🔥'


def get_help_text():
    return HELP_TEXT


def get_github_url():
    return GITHUB_PROJECT_URL


commands = {
    '!quote': get_random_quote,
    '!help': get_help_text,
    '!github': get_github_url
}
