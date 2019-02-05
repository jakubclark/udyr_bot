import json
from random import randrange

import discord

help_text = '''
Udyr-Bot Commands:
        !quote  - Random Udyr quote
        !help   - This help message
        !github - Get the GitHub address of the project'''

with open('udyr_quotes.json') as f:
    data = json.load(f)
quotes = data['quotes']


def get_random_quote():
    return quotes[randrange(len(quotes))]


def get_help_text():
    return help_text


def github_link():
    return 'https://github.com/jakubclark/udyr_bot'


commands = {
    '!quote': get_random_quote,
    '!help': get_help_text,
    '!github': github_link,
}

client: discord.Client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as', end=' ')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    content = message.content.lower()

    if not content.startswith('!') or message.author == client.user:
        return

    if content.startswith('!quote'):
        func = commands['!quote']

    elif content.startswith('!help'):
        func = commands['!help']

    elif content.startswith('!github'):
        func = commands['!github']

    else:
        func = commands['!help']

    res = func()
    await client.send_message(message.channel, res)


commands = {
    '!quote': get_random_quote,
    '!github': github_link,
    '!help': get_help_text
}


def create_client():
    return client
