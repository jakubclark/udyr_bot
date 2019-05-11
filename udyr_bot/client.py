from logging import getLogger

import discord

from .commands import commands
from .constants import BOT_NAME, COMMAND_PREFIX

log = getLogger(__name__)


class Client(discord.Client):

    def __init__(self):
        super().__init__()

    async def on_ready(self):
        log.info('Logged in as')
        log.info(self.user.name)
        log.info(self.user.id)
        log.info('------')
        servers = [server.name for server in self.servers]
        log.info(f'Servers `{BOT_NAME}` is present in: {servers}')

    async def on_resumed(self):
        log.info('Bot has been resumed')

    async def on_message(self, message: discord.Message):
        author: discord.Member = message.author

        if isinstance(author, discord.Member):
            # server
            server: discord.Server = author.server
            log.info(
                f'Server: {server} Chanel: {message.channel.name} Author: {author} Message: {message.content}')

        first_word = message.content.split()[0]
        cmd = message.content.split()[1:]

        if not first_word.startswith(COMMAND_PREFIX):
            return
        try:
            func = commands[first_word]
        except KeyError:
            return

        res = func(cmd)

        await self.send_typing(message.channel)
        await self.send_message(message.channel, res)

    async def on_reaction_add(self, reaction: discord.Reaction, member: discord.User or discord.Member):
        message: discord.Message = reaction.message
        emoji: discord.Emoji = reaction.emoji
        try:
            log.info(f'Adding {reaction.emoji} to {reaction.message.content}')
            await self.add_reaction(message, emoji)
        except discord.Forbidden:
            log.info(f'Forbidden to add reaction')
        except discord.NotFound:
            log.info(f'Did not find the emoji')
        except discord.HTTPException:
            log.info(f'HTTPExcetion when adding reaction')

    async def on_member_join(self, member: discord.Member):
        log.info(f'{member} has joined {member.server}')
        await self.add_animal_role(member)

    async def on_server_join(self, server: discord.Server):
        log.info(f'{BOT_NAME} joined {server.name}')

    async def on_error(self, event, *args, **kwargs):
        log.info(f'Unhandled error for event: {event}, args={args}, kwargs={kwargs}')
