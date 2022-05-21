import os
import discord

# Initiate intents for the bot
# These lines grant the bot permissions, such as:
# Viewing the list of members
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# Declare global variables, dicts and what have you.
channel = discord.TextChannel
method_dic = {"register": register_member, "unregister": unregister_member}

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

		# Fetches the channel that we'll use to
		channel = client.get_channel(976299911274459146)

		try:
				await channel.send('books')
		except AttributeError:
				print(
						'~uwu~ :: It looks like that channel wannel doesn\'t existy wisty! :: ~owo~'
				)


# Method to register a member to the book club
async def register_member():
	# TODO: Register member
	try:
		channel = client.get_channel(976299911274459146)
		await channel.send('TODO: Register user to the club');
	except AttributeError:
		print('AttributeErr')


# Method to leave the book club
async def unregister_member():
	# TODO: Unregister
	try:
		channel = client.get_channel(976299911274459146)
		await channel.send('TODO: Unregister user from the club');
	except AttributeError:
		print('AttributeErr')


@client.event
async def on_message(message):
	if message.author == client.user:
				return

	print(f'We just got a letter!')

	if message.content.startswith("book!"):
		split = message.content.split(" ")

		print(f'The delimiters gave us this: {split}')

		if split[1] in method_dic:
			await method_dic[split[1]]()
			print(f'The command is {split[1]}, calling method {method_dic[split[1]]}')
		else:
			print(f'The command {split[1]} does not coincide with any method')



client.run(bot_token)
