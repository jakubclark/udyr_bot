import json
import os

from discord import Color

with open('data/udyr_quotes.json') as f:
    QUOTES = json.load(f)

BOT_NAME = 'Udyr Bot'
COMMAND_PREFIX = '!'

DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
RIOT_DEV_API_KEY = os.environ['RIOT_DEV_API_KEY']


HELP_TEXT = '\n '.join([
    '!quote  - Random Udyr quote',
    '!help   - This help message',
    '!github - Get the GitHub address of the project',
    '!summ   - Get Ranked Information for a summoner: `!summ Donger Dingo`, `!summ yassuo --region NA`',
    '!game   - Get Information for a currently playing game: `!game Donger Dingo`, `!game Imaqtpie --region NA`'
])
QUOTES_LEN = len(QUOTES)
GITHUB_PROJECT_URL = 'https://github.com/jakubclark/udyr_bot'


BASE_EMBED = {
    'color': Color.dark_green().value,
    'thumbnail': {
        'url': 'https://raw.githubusercontent.com/jakubclark/udyr_bot/master/data/udyr1.png',
        'height': 30,
        'width': 30
    }
}
