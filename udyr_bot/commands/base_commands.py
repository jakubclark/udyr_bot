from random import randrange

from discord import Embed

from ..constants import (BASE_EMBED, GITHUB_PROJECT_URL, HELP_TEXT, QUOTES,
                         QUOTES_LEN)


def get_random_quote(*args):
    quote = f'🔥{QUOTES[randrange(QUOTES_LEN)]}🔥'
    embed_content = BASE_EMBED.copy()
    embed_content['description'] = quote
    return Embed.from_dict(embed_content)


def get_help_text(*args):
    embed_content = BASE_EMBED.copy()
    embed_content['title'] = 'Udyr Bot Commands'
    embed_content['description'] = HELP_TEXT
    return Embed.from_dict(embed_content)


def get_github_url(*args):
    return GITHUB_PROJECT_URL
