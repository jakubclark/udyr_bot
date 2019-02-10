from logging import getLogger

import discord

from .commands import handle_message, handle_member_join, handle_reaction_add, handle_server_join

log = getLogger(__name__)

client: discord.Client = discord.Client()


@client.event
async def on_ready():
    log.info('Logged in as', end=' ')
    log.info(client.user.name)
    log.info(client.user.id)
    log.info('------')


@client.event
async def on_resumed():
    log.info('Bot has been resumed')


@client.event
async def on_message(message: discord.Message):
    if message.channel.type == discord.ChannelType.text:
        await handle_message(client, message)


@client.event
async def on_reaction_add(reaction: discord.Reaction, member: discord.User or discord.Member):
    await handle_reaction_add(client, reaction, member)


@client.event
async def on_member_join(member: discord.Member):
    await handle_member_join(client, member)


@client.event
async def on_server_join(server: discord.Server):
    await handle_server_join(client, server)


@client.event
async def on_error(event, *args, **kwargs):
    log.info(f'Unhandled error for event: {event}')
