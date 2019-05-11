from .base_commands import get_random_quote, get_help_text, get_github_url
from .summoner_info import get_summoner_info

commands = {
    '!quote': get_random_quote,
    '!help': get_help_text,
    '!github': get_github_url,
    '!summ': get_summoner_info
}
