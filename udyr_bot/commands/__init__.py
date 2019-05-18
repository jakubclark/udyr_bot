from .base_commands import get_github_url, get_help_text, get_random_quote
from .summoner_info import get_game_info, get_summoner_info

commands = {
    '!quote': get_random_quote,
    '!help': get_help_text,
    '!github': get_github_url,
    '!summ': get_summoner_info,
    '!game': get_game_info
}
