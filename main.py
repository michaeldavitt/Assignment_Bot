import discord
import os
import pandas as pd
import datetime
import openpyxl
from keep_alive import keep_alive


def days_till_due_calc(row):
  """Function to calculate the number of days until an assignemnt is due
  
  Check that the Date in the row provided is a datetime.datetime object
  to_excel automatically converts dates into datetime.datetime objects
  If it is not a datetime.datetime object, return 365 as the default
  """

  # When the exact date is not known, set it to 365
  if type(row["Date"]) != datetime.datetime:
    return 365

  # Get the due date and todays date in the date format (without time)
  due_date = row["Date"].date()
  today = datetime.date.today()

  # Return the difference between the two as a number of days (without time)
  return (due_date - today).days

TOKEN = os.environ["TOKEN"]

client = discord.Client()

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  # Ignore the message if it came from the bot
  if message.author == client.user:
    return

  # Only display assignments and days until due when the user requests then
  if message.content.startswith("$assignments") or message.content.startswith("$Assignments"):

    # Need to read in the xlsx file containing assignment information
    df = pd.read_excel("Assignments.xlsx")
    
    # Need to add a column for number of days until due
    df["Days_till_due"] = df.apply(lambda row: days_till_due_calc(row), axis = 1)

    # Sort the dataframe rows by days until the assignment is due
    df = df.sort_values(by = "Days_till_due")

    # Create an empty string for the message
    msg = ""

    # Go through the rows in the dataframe and print them to the channel
    for index, row in df.iterrows():

      # Don't print out the row if it is blank or if the due date is unknown
      if row["Assignment"] != "nan" and row["Days_till_due"] != 365 and row["Days_till_due"] >= 0:

        # Construct the message using string concatenation
        msg += str(row["Assignment"]) + " due in " + str(row["Days_till_due"]) + " days. Part of the module " + str(row["Module"] + ". Worth " + str(round(row["Percentage"] * 100)) + "% of the final grade.\n")

    # Print the message
    await message.channel.send(msg)

keep_alive()
client.run(TOKEN)