from logging import getLogger

import discord

from .commands import commands
from .constants import BOT_NAME, COMMAND_PREFIX

log = getLogger(__name__)


class Client(discord.Client):

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
        member: discord.Member = message.author
        server: discord.Server = member.server
        first_word = message.content.split()[0]

        log.info(
            f'Server: {server} Chanel: {message.channel.name} Member: {member} Message: {message.content}')
        if not first_word.startswith(COMMAND_PREFIX):
            return
        try:
            func = commands[first_word]
        except KeyError:
            func = commands['!help']

        res = func()

        await self.send_typing(message.channel)
        await self.send_message(message.channel, res)

    async def on_reaction_add(self, reaction: discord.Reaction, member: discord.User or discord.Member):
        log.info(f'{reaction} added by {member} to {reaction.message.content}')

    async def on_member_join(self, member: discord.Member):
        log.info(f'{member} has joined {member.server}')
        await self.add_animal_role(member)

    async def on_server_join(self, server: discord.Server):
        log.info(f'{BOT_NAME} joined {server.name}')

    async def on_error(self, event, *args, **kwargs):
        log.info(f'Unhandled error for event: {event}')

    async def add_animal_role(self, member: discord.Member):
        for role in member.server.roles[1:]:  # Ignore @everyone
            if role.name == 'Animals':
                log.info(f'Adding the `Animals` role for {member}')
                await self.add_roles(member, role)
                break
        else:
            log.info('Did not find the `Animals` role!')


client = Client()
