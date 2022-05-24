import os
import discord
import requests
import json

# Initiate intents for the bot
# These lines grant the bot permissions, such as:
# Viewing the list of members
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# Declare global variables, dicts and what have you.
channel = discord.TextChannel

# Set this to true if you feel like debugging anything
debugging = True

# END declaring global variables


# Bot Token stored in Environment Variables
bot_token = os.environ['TOKEN']

# Initialize client. Used for all sorts of everything
client = discord.Client(intents=intents)


# Event that activates as soon as the bot wakes up
# Could have it send a "hello" message, could have it check databases, etc.
@client.event
async def on_ready():
		print(f'We have logged in as {client.user}')


# Method to register a member to the book club
async def register_member(message):
	try:
		channel = message.channel

		# Get references to the member and their guild here
		# Guild is useful for managing roles & perms
		member = message.author
		member_guild = member.guild

		# Makes sure the bookie role doesn't exist already
		role_exists = discord.utils.get(member_guild.roles, name="Bookie")

		# If bookie role doesn't exist, then create it:
		if not role_exists:
			await member_guild.create_role(name="Bookie", colour=discord.Colour(0xF88D89))


		# Make sure member doesn't already have the role:
		has_role = discord.utils.get(member.roles, name="Bookie")

		# If member has the role, scold them.
		if has_role:
			await channel.send(f'You\'re already part of the book club, silly willy!')
		else:
			print(f'Author: {member}')

			try:
				book_role = discord.utils.get(member_guild.roles, name="Bookie")

				print(f'Book role: {book_role}')

				await member.add_roles(book_role)

				await channel.send(f'Welcome to the club, {member.mention}!')
			except AttributeError:
				await channel.send('oh shit oh fuck something bad happened')
	except AttributeError:
		print(AttributeError)


# Method to leave the book club
async def unregister_member(message):
	try:
		channel = message.channel

		member = message.author

		has_role = discord.utils.get(member.roles, name="Bookie")

		if has_role:
			book_role = discord.utils.get(member.roles, name="Bookie")
			await member.remove_roles(book_role)

			await channel.send(f'I-it\'s not like I\'m mad to see you go or anything! Just leave already....')
		else:
			await channel.send(f'You need to be part of the club to leave it, asswipe.')
	except AttributeError:
		print('AttributeErr')


# Lookup book information with Google API
async def book_lookup(message):
	# TODO: Actually fetch book information from Google

	try:
		channel = message.channel

		member = message.author

		split_str = message.content.split(" ", 2)

		await channel.send(f'So you\'re trying to find information on the book \"{split_str[2]}\", is that correct? (Don\'t actually reply I won\'t say shit back)')

		lookup_test = requests.get('https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&maxResults=1&key=')

		print(f'{lookup_test.json()["items"][0]["volumeInfo"]["description"]}')

	except AttributeError:
		print('AttributeErr')


# "Help" menu
async def help(message):
	channel = message.channel

	await channel.send("No.")

# Dictionary that holds commands
# The key is each command (ex: register, schedule)
# Each key points to its corresponding function
method_dic = {"join": register_member,
			  "leave": unregister_member,
			  "lookup": book_lookup,
				"help": help}


@client.event
async def on_message(message):
	if message.author == client.user:
				return

	print(f'We just got a letter!')

	if message.content.startswith("book!"):
		split = message.content.split(" ")

		print(f'The delimiters gave us this: {split}')

		if split[1] in method_dic:
			await method_dic[split[1]](message)
			print(f'The command is {split[1]}, calling method {method_dic[split[1]]}')
		else:
			print(f'The command {split[1]} does not coincide with any method')



client.run(bot_token)
