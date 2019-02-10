from logging import getLogger
from random import randrange

import discord

from .constants import GITHUB_PROJECT_URL, HELP_TEXT, QUOTES, QUOTES_LEN, BOT_NAME

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


async def add_animal_role(client: discord.Client, member: discord.Member):
    for role in member.server.roles[1:]:
        if role.name == 'Animals':
            log.info(f'Adding the `Animals` role for {member}')
            await client.add_roles(member, role)
            break
    else:
        log.info('Did not find the `Animals` role!')


async def handle_message(client: discord.Client, message: discord.Message):
    member: discord.Member = message.author
    server = member.server
    content = message.content
    first_word = content.split()[0]

    log.info(f'Server: {server} Member: {member} Message: {message.content}')
    if not first_word.startswith('!'):
        return
    try:
        func = commands[first_word]
    except KeyError:
        func = commands['!help']

    res = func()

    await client.send_typing(message.channel)
    await client.send_message(message.channel, res)


async def handle_reaction_add(client: discord.Client, reaction: discord.Reaction, member: discord.Message or discord.User):
    log.info(f'{reaction} added by {member} to {reaction.message.content}')


async def handle_member_join(client: discord.Client, member: discord.Member):
    log.info(f'{member} has joined {member.server}')
    await add_animal_role(member, client)


async def handle_server_join(client: discord.Client, server: discord.Server):
    log.info(f'{BOT_NAME} joined {server.name}')
