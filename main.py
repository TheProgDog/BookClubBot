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

# Event that activates as soon as the bot wakes up
# Could have it send a "hello" message, could have it check databases, etc.
@client.event
async def on_ready():
		print(f'We have logged in as {client.user}')

		# Fetches the channel that we'll use to
		channel = client.get_channel(938205761027317830)

		try:
				await channel.send('fuck')
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


client.run(bot_token)
