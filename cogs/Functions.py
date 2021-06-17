import discord
import os
from discord.ext import commands, tasks
import asyncio
from tabulate import tabulate
import random

class Functions(commands.Cog):

	#Variables
	count = [0] * 10
	flags = {
    	1: "tuctf{Test_Flag 1}",
    	2: "tuctf{Test_Flag 2}",
		3: "tuctf{Test_Flag 3}",
		4: "tuctf{Test_Flag 4}",
		5: "tuctf{Test_Flag 5}",
		6: "tuctf{Test_Flag 6}",
		7: "tuctf{Test_Flag 7}",
		8: "tuctf{Test_Flag 8}",
		9: "tuctf{Test_Flag 9}",
		10: "tuctf{Test_Flag 10}"
	}
	gifs_correct = [
		"https://gph.is/g/466rD0q",	#0 You Got This
		"https://gph.is/g/4gBQ0wA",	#1 Boo-yah
	]
	gifs_wrong = [
		"https://gph.is/g/ZO0rLYg",	#0 Searching
		"https://gph.is/g/apKb7B3",	#1 Congrats, you're Wrong
		"https://gph.is/1LRBUQe",	#2 Don't even trip dawg
	]
	isflag = False
	listPrime = []
	score = [0] * 6
	score_list = {
    	1: 100,
    	2: 90,
		3: 80,
		4: 70,
		5: 60,
		6: 50
	}
	solved_flags = [
		[], [], [], [], [], []
	]
	teams = [
		"Obscurial",
		"Holoquin",
		"Tyronical",
		"GhostGoblins",
		"Strafers",
		"OceanMasters"
	]
	
	async def updateScoreboard(self, ctx, flag):
		self.isflag = False
		for i in range(10):
			if flag == self.flags[i+1]:
				self.isflag = True
				self.count[i] += 1
				await ctx.send(random.choice(self.gifs_correct))
				await ctx.send("Flag " + str(i+1) + " Accepted")
				if self.count[i] == 1:
					await ctx.send("https://gph.is/g/ZnQJeNA")
				for j in range(6):
					if str(ctx.channel) == self.teams[j+1]:
						self.solved_flags[j].append(i+1)
						self.solved_flags[j].sort()
		
		if not self.isflag:
			await ctx.send(random.choice(self.gifs_wrong))
			await ctx.send("buh-boo!! That's not the right flag")
		
		for i in range(6):
			self.score[i] = 0
			for j in range(10):
				if j+1 in self.solved_flags[i]:
					ans = self.score_list[self.count[j]]
					self.score[i] += ans	

	#Constructor
	def __init__(self, client):
		self.client = client

	#Tasks
	@tasks.loop(seconds=1, count=1)
	async def displayScoreboard(self, ctx):
		self.listPrime = []
		for i in range(6):
			temp = [i+1, self.teams[i], self.score[i]]
			self.listPrime.append(temp)

		temp = tabulate(self.listPrime,  headers = ["Sr. No.", "Team", "Score"], tablefmt = "fancy_grid", numalign = "center")
		await ctx.send("```css\n" + temp + "\n```")

	#Events
	@commands.Cog.listener()
	async def on_ready(self): 
		print(f"Application Bot Online as {self.client.user}")
		activity_type = discord.ActivityType.listening
		activity = discord.Activity(type=activity_type, name="$help")
		status = discord.Status.online
		await self.client.change_presence(activity=activity, status = status)
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		await ctx.send("https://gph.is/g/ZxP6eRl")
		if(isinstance(error, commands.CommandNotFound)):
			await ctx.send("My program directives don't allow me to do that. Use $help to get a list of valid commands.")
		if(isinstance(error, commands.MissingPermissions)):
			await ctx.send("You don't have the permission to do that. Contact a MOD, please.")
	
	#Commands
	@commands.command()
	async def help(self, ctx):
		embed = discord.Embed( colour = ctx.author.colour )
		embed.set_author(name="List of Commands", icon_url = os.environ['logo_url'])

		embed.add_field(name = "$flag / $f", value = "Ready to accept the flag", inline = False)

		embed.set_footer(text=f"Help requested by: {ctx.author.display_name}")

		await ctx.send(embed=embed)

	@commands.command(aliases=["p"])
	async def ping(self, ctx):
		await ctx.send(f"Latency: {round(self.client.latency * 1000)} ms")
	
	@commands.command(aliases=["dsc"])
	async def displaysc(self, ctx):
		await ctx.channel.purge(limit = 1)
		await self.displayScoreboard.start(ctx)

	@commands.command(aliases=["c"])
	@commands.has_permissions(manage_messages = True)
	async def clear(self, ctx, n = 1):
		if n == 0:
			return
		else:
			await ctx.channel.purge(limit = (n + 1))

	@commands.command()
	async def sendgif(self, ctx):
		for i in range(9):
			await ctx.send(self.gifs[i])

	@commands.command(aliases=["f"])
	async def flag(self, ctx):
		embed = discord.Embed(
			title="Command for flag insertion",
			description="The format is\ntuctf{your_flag_here}\n||This request will timeout in 120 seconds||"
		)
		sent = await ctx.send(embed=embed)

		try:
			msg = await self.client.wait_for(
				"message",
				check = lambda message: message.author == ctx.author and message.channel == ctx.channel,
				timeout=120				
			)

			if msg.content:
				await ctx.send("Message received")
				if msg.content.startswith("tuctf"):
					await self.updateScoreboard(ctx, msg.content)
				else:
					await ctx.send("Please enter the flag in the given format")

		except asyncio.TimeoutError:
			await sent.delete()
			await ctx.send("Timeout. Send a request again ($flag)", delete_after=10)
		
def setup(client):
	client.add_cog(Functions(client))
