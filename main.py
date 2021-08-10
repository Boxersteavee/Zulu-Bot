import os
import asyncio
import traceback
import sys
from discord.ext import commands
from discord.ext import tasks
import discord
import os
import random

TOKEN = os.environ['TOKEN']

    

zulu = commands.Bot(command_prefix = 'z.')

@zulu.event
async def on_ready():
    await zulu.change_presence(activity=discord.Game(name="z.cmds for a list of commands."))
    print('{0.user} is ready'.format(zulu))
    

@zulu.event
async def on_command_error(ctx, error):
     if isinstance(error, commands.CommandNotFound):
      NotFound = discord.Embed(
            title = 'Command does not exist!',
            description = 'I did not recognize the command you sent. Was it a typo? Try z.cmds to see a list of all commands',
            colour = discord.Colour.blue()

      )
      NotFound.set_footer(text='Did you make a typo?')
      NotFound.set_author(name='No such command')


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
@zulu.command(aliases=['commands', 'commandlist'])
async def cmds(ctx):
    global helpembed

    await ctx.send(embed=helpembed)

class MyHelp(commands.HelpCommand):
   #code that makes z.help work
    async def send_bot_help(self, mapping):
        await self.context.send(embed=helpembed)

@zulu.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(zulu.latency * 1000)}ms')
    

zulu.help_command = MyHelp()
zulu.run(TOKEN)
