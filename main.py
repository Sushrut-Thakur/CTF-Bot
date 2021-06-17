from discord.ext import commands
import os
from keep_alive import keep_alive

import warnings
warnings.filterwarnings("ignore") #Ignores warnings due to deprecated libraries/functions

client = commands.Bot(command_prefix = '$')
client.remove_command("help")

@client.command()
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")
	await ctx.send(f"Extension {extension} loaded")

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")
	await ctx.send(f"Extension {extension} unloaded")

@client.command(aliases=["r"])
async def reload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")
	client.load_extension(f"cogs.{extension}")
	await ctx.send(f"Extension {extension} reloaded")

for file in os.listdir("./cogs"):
	if file.endswith(".py"):
		client.load_extension(f"cogs.{file[:-3]}")

keep_alive()	#Function call to the bot uptime service
client.run(os.getenv('TOKEN'))
