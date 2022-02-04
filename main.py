import os
import asyncio
import traceback
import sys
from discord.ext import commands
from discord.ext import tasks
from discord.commands import Option
import discord
import os
import random
import requests
from dotenv import load_dotenv
import time

from discord.ext.commands.errors import BadLiteralArgument

#TOKEN = os.environ['TOKEN']

load_dotenv()

zulu = commands.Bot(command_prefix = 'z.')

test_servers = [764981968579461130, 798180194049196032]

@zulu.event
async def on_ready():
    await zulu.change_presence(activity=discord.Game(name="z.cmds for a list of commands."))
    print('{0.user} is ready'.format(zulu))
    

@zulu.event
async def on_command_error(ctx, error):
     if isinstance(error, commands.CommandNotFound):
      NotFound = discord.Embed(
            title = 'I use slash commands now',
            description = 'I have evolved with discord, i no longer use prefix commands as discord have made a new fancy feature called slash commands, press the `/` key see!',
            colour = discord.Colour.blue()

      )
      NotFound.set_footer(text='I am the best discord bot, you cannot change my mind as i was coded to say this.')


      await ctx.send(embed=NotFound)
      if isinstance(error, commands.MissingPermissions):
        NoPerms = discord.Embed(
            title = 'No permissions!',
            description = 'You do not have permission to do that command!',
            colour = discord.Colour.red()

        )
        NoPerms.set_footer(text='You can\'t do that command')
        NoPerms.set_author(name='You need Permission to run that command.')
        await ctx.send(embed=NoPerms)
      if isinstance(error, UnboundLocalError):
        return
      else:
        raise error

#embed for help command.
helpembed = discord.Embed(
  title = 'Commands List',
  description = 'Here is a list of commands.',
  colour = discord.Colour.blue()
    
  )

helpembed.set_footer(text='This is the best discord bot')
helpembed.set_author(name='ZuluBot commands:')
helpembed.add_field(name='Ping!', value='Shows the ping of the bot')
helpembed.add_field(name='Help', value='Shows this command.')

@zulu.slash_command(guild_ids=test_servers)  # create a slash command for the supplied guilds
async def help(ctx):
    await ctx.defer()
    """Sends the help command"""  # the command description can be supplied as the docstring
    await ctx.respond(f"Hello <@{ctx.author.id}>!,", embed=helpembed)

@zulu.slash_command(guild_ids=test_servers)  # create a slash command for the supplied guilds
async def hello(ctx):
    """:wave:"""
    await ctx.defer()
    """Say hello to the bot"""  # the command description can be supplied as the docstring
    await ctx.respond(f"Hello {ctx.author.mention}!")


@zulu.slash_command(guild_ids=test_servers)
async def ping(ctx):
  await ctx.defer()
  """ping the discord API"""
  pingtime = round(zulu.latency * 1000)
  pingembed = discord.Embed(
  title = 'Pong!',
  description = 'Ping time:' + (str(pingtime)) + 'ms',
  colour = discord.Colour.blue()

  )

  pingembed.set_footer(text='This is the best discord bot')
 
  await ctx.respond(embed=pingembed)
    
@zulu.slash_command()
async def srvstatus(
    ctx,
    ip: Option(str, "Enter the server IP", required=True),
):
    """Ping minecraft servers."""
    temprespond = discord.Embed(
      title = f'Loading Status for {ip}'
    )

    interaction = await ctx.respond(embed=temprespond)
    
    
    r = requests.get(f'https://api.mcsrvstat.us/2/{ip}')

    API_Response = r.json()

    if API_Response["online"] == False:
      finalrespond = discord.Embed(
      title = f'Status of {ip}'
      )
      finalrespond.set_footer(text='Information from https://api.mcsrvstat.us')
      finalrespond.add_field(name='IP', value=f"`{API_Response['ip']}`", inline=True)
      finalrespond.add_field(name='Port', value=f"`{API_Response['port']}`", inline=True)
      finalrespond.add_field(name='Online', value=f"`{API_Response['online']}`", inline=True)
      finalrespond.add_field(name='Hostname', value=f"`{API_Response['hostname']}`", inline=True)
      await interaction.edit_original_message(embed=finalrespond)

    else:
      finalrespondon = discord.Embed(
      title = f'Status of {ip}'
      )
      finalrespondon.set_footer(text='Information from https://api.mcsrvstat.us')
      finalrespondon.add_field(name='IP', value=f"`{API_Response['ip']}`", inline=True)
      finalrespondon.add_field(name='Port', value=f"`{API_Response['port']}`", inline=True)
      finalrespondon.add_field(name='Online', value=f"`{API_Response['online']}`", inline=True)
      finalrespondon.add_field(name='Hostname', value=f"`{API_Response['hostname']}`", inline=True)
      finalrespondon.add_field(name='Version', value=f"`{API_Response['version']}`", inline=True)
      finalrespondon.add_field(name='Player Count', value=f"`{API_Response['players']['online']}/{API_Response['players']['max']} `", inline=True)
      finalrespondon.add_field(name='MOTD', value=f"`{API_Response['motd']['clean']} `", inline=True)
      finalrespondon.set_image(url=f"https://api.mcsrvstat.us/icon/{ip}")
      await interaction.edit_original_message(embed=finalrespondon)

@zulu.slash_command(guild_ids=test_servers)
async def hug(ctx,
              member: discord.commands.Option(discord.Member, 'Who you wanna hug', required=False),
              reason: discord.commands.Option(str, 'Why you want to hug them', required=False)):
    """Hugggszzz!"""
    await ctx.defer()
    r = requests.get(f'https://nekos.life/api/v2/img/hug')
    hug_json = r.json()
    hugembed=discord.Embed(title="Have a hug", description=("You need it"), color=0xff0000)
    hugembed.set_footer(text='Gif from https://nekos.life/api/v2/img/hug')
    hugembed.set_image(url=f"{hug_json['url']}")
    if reason is None:
      reason = "You need it!"
    elif member is None:
      await ctx.respond(f"Whoever you are, have a hug {reason}", embed=hugembed)
    else:
      await ctx.respond(f"{member.mention}, have a hug, {reason}", embed=hugembed)



zulu.run(os.getenv("TOKEN"))
