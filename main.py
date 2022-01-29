import discord
import os

TOKEN = os.environ["TOKEN"]

client = discord.Client()

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("$assignments"):
    await message.channel.send("Assignments Due:")
    # Need to read in the CSV file containing assignment information
    # Need to store this CSV file as a dataframe
    # Dataframe columns: Assignment, Module, Date
    # Need to add a column for number of days until due

client.run(TOKEN)