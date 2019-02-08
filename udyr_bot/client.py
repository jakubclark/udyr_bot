from random import randrange

import discord

from .constants import GITHUB_PROJECT_URL, HELP_TEXT, QUOTES, QUOTES_LEN


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


def create_client():
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

        if not content.startswith('!') or len(content) < 2 or message.author == client.user:
            return

        first_word = content.split()[0]
        try:
            func = commands[first_word]
        except KeyError:
            func = commands['!help']

        res = func()

        await client.send_typing(message.channel)
        await client.send_message(message.channel, res)

    return client
