import os
import discord
import random

#client = discord.Client()

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
# TODO: Fix this, actually add Discord Bot Token to environment variables
bot_token = os.environ['TOKEN']

# Initialize client. Used for all sorts of everything
client = discord.Client(intents=intents)

# TODO: Initiate variable that keeps track of probability
# of the bot using @everyone. Variable should be able to
# persist between Bot lifecycles as the bot crashes and
# boots itself back up.





# Methods for book club specific functionalities

# Method to register a member to the book club
async def register_member():
	# TODO: Register member
	await channel.send('TODO: Register');


# Method to leave the book club
async def unregister_member():
	# TODO: Unregister
	await channel.send('TODO: Unregister');


method_dic = {"register": register_member, "unregister": unregister_member}

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

				danny_pikmin = client.get_user(102610839558688768)

				try:
						print(
								f'Successfully found {danny_pikmin}. Use the debug console to find out more information.\n{danny_pikmin.activity.name} {danny_pikmin.activity.large_image_text} {danny_pikmin.activity.small_image_text}\n{danny_pikmin.activity.status} {danny_pikmin.activity.type} {danny_pikmin.activity.details}'
						)
				except AttributeError:
						print("No activity is detected.")
						pass

@client.event
async def on_message(message):
	if message.author == client.user:
				return

	print(f'We just got a letter!')

	if message.content.startswith("book!"):
		split = message.content.split(" ")

		print(f'The delimiters gave us this: {split}')

		if split[1] in method_dic:
			method_dic[split[1]]
		else:
			print(f'The command {split[1]} does not coincide with any method')



client.run(bot_token)
