import json
import os

with open('udyr_quotes.json') as f:
    data = json.load(f)

BOT_NAME = 'Udyr Bot'
COMMAND_PREFIX = '!'

DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
RIOT_DEV_API_KEY = os.environ['RIOT_DEV_API_KEY']

HELP_TEXT = '''
Udyr-Bot Commands:
        !quote  - Random Udyr quote
        !help   - This help message
        !github - Get the GitHub address of the project
        !summ - Get Ranked Information for a summoner: `!summ Donger Dingo`, `!summ yassuo --region NA`'''
QUOTES = data['quotes']
QUOTES_LEN = len(QUOTES)
GITHUB_PROJECT_URL = 'https://github.com/jakubclark/udyr_bot'
