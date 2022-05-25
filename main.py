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
			try:
				book_role = discord.utils.get(member_guild.roles, name="Bookie")

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

		split_str = message.content.split(" ", 2)

		# await channel.send(f'So you\'re trying to find information on the book \"{split_str[2]}\", is that correct? (Don\'t actually reply I won\'t say shit back)')

		req_base = "https://www.googleapis.com/books/v1/volumes?q=intitle:"
		req_search = split_str[2].replace(" ", "+")

		req_whole = req_base + req_search + "&maxResults=10&key="

		print(req_whole)

		result = requests.get(req_whole).json()

		await print_book(split_str[2], result["items"][0]["volumeInfo"])

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


# Print method for book information
async def print_book(search, volume):
	
	await channel.send(f'Search results for: \"{search}\": \n\n__**Author**__: {volume["authors"][0]}\n__**Title**__: \"{volume["title"]}\"
	\n__**Description**__:{volume["description"]}\n__**Pages**__: {volume["pageCount"]}\n__**ISBN-10**__: {volume["industryIdentifiers"][1]["identifier"]}
	\n__**ISBN-13**__: {volume["industryIdentifiers"][0]["identifier"]}\n{volume["imageLinks"]["thumbnail"]}')

# Reacting to reactions
@client.event
async def on_reaction_add(reaction, user):
	if user == client.user:
		return
	channel = reaction.channel

	await channel.send(reaction)


@client.event
async def on_message(message):
	if message.author == client.user:
				return

	if message.content.startswith("book!"):
		split = message.content.split(" ")

		if split[1] in method_dic:
			await method_dic[split[1]](message)
		else:
			await channel.send(f'The command {split[1]} does not coincide with any method')



client.run(bot_token)
