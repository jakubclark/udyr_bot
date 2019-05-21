from logging import getLogger

import discord

from udyr_bot.commands.summoner_info import RiotGamesDAO
from .commands import commands
from .config import Config
from .constants import BOT_NAME, COMMAND_PREFIX

log = getLogger(__name__)


class Client(discord.Client):
    def __init__(self):
        self.riot_games_dao = RiotGamesDAO(Config.get('riot_dev_api_key'))
        self.commands = commands
        self.commands['!summ'] = self.riot_games_dao.get_summoner_info
        self.commands['!game'] = self.riot_games_dao.get_game_info
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
        if message.author == self.user:
            return
        try:
            await self._on_message(message)
        except Exception as e:
            log.error(f'Eror when processing message. e={e}')

    async def _on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        split_conent = message.content.split()
        first_word = split_conent[0]

        if not first_word.startswith(COMMAND_PREFIX):
            return

        cmd = message.content.split()[1:]
        author: discord.Member or discord.User = message.author
        channel: discord.TextChannel = message.channel

        if isinstance(author, discord.Member):
            guild: discord.Guild = author
            log.info(
                f'Guild: {guild}, Channel: {message.channel.name}, Author: {author}, Message: {message.content}')
        else:
            log.info(
                f'Author: {author}, Message: {message.content}')

        try:
            func = commands[first_word]
        except KeyError:
            return

        res = func(cmd)

        if isinstance(res, discord.Embed):
            await channel.send(embed=res)
        else:
            await channel.send(content=res)

    async def on_reaction_add(self, reaction: discord.Reaction, member: discord.User or discord.Member):
        message: discord.Message = reaction.message
        emoji: discord.Emoji = reaction.emoji

        try:
            log.info(f'Adding {emoji} to {reaction.message.content}')
            await message.add_reaction(emoji)
        except discord.Forbidden:
            log.info(f'Forbidden to add reaction')
        except discord.NotFound:
            log.info(f'Did not find the emoji')
        except discord.HTTPException:
            log.info(f'HTTPExcetion when adding reaction')

    async def on_server_join(self, server: discord.Guild):
        log.info(f'{BOT_NAME} joined {server.name}')

    async def on_error(self, event, *args, **kwargs):
        log.info(
            f'Unhandled error for event: {event}, args={args}, kwargs={kwargs}')
