import json
import os

with open('udyr_quotes.json') as f:
    data = json.load(f)

BOT_NAME = 'Udyr Bot'
COMMAND_PREFIX = '!'

DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']

HELP_TEXT = '''
Udyr-Bot Commands:
        !quote  - Random Udyr quote
        !help   - This help message
        !github - Get the GitHub address of the project'''
QUOTES = data['quotes']
QUOTES_LEN = len(QUOTES)
GITHUB_PROJECT_URL = 'https://github.com/jakubclark/udyr_bot'
