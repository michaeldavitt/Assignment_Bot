import discord
import os
import pandas as pd
import datetime
import openpyxl
from keep_alive import keep_alive


def days_till_due_calc(row):
  """Function to calculate the number of days until an assignemnt is due
  
  Check that the Date in the row provided is a Timestamp object
  to_excel automatically converts dates into Timestamp objects
  If it is not a Timestamp object, return 365 as the default
  """

  # When the exact date is not known, set it to 365
  if type(row["Date"]) != pd._libs.tslibs.timestamps.Timestamp:
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

      # Don't print out the row if it is blank, if days till due is unknown, or if the date is in the past
      if row["Assignment"] != "nan" and row["Days_till_due"] != 365 and row["Days_till_due"] >= 0:

        # Construct the message using string concatenation
        new_msg = str(row["Assignment"]) + " due in " + str(row["Days_till_due"]) + " days. Part of the module " + str(row["Module"] + ". Worth " + str(round(row["Percentage"] * 100)) + "% of the final grade.\n\n")

        # Split longer messages due to Discord's character limit
        if len(msg + new_msg) > 2000:
          # Send a section of the message
          await message.channel.send(msg)

          # Initialise the next message section
          msg = ""

        # Add the new message onto the original message
        msg += new_msg

    # Print the final message segment
    await message.channel.send(msg)

# For keeping the bot running after I've turned off my machine
keep_alive()
client.run(TOKEN)