import nextcord
import os
import random
import datetime
import asyncio
import typing
from nextcord.ext import commands
from keep_alive import keep_alive
import time  # Import the time module

print("""
.▄▄▄  ▄• ▄▌ ▄▄▄·  ▐ ▄ ▄▄▄▄▄▄• ▄▌• ▌ ▄ ·.      ▄▄ • ▄▄▄ . ▐ ▄ 
▐▀•▀█ █▪██▌▐█ ▀█ •█▌▐█•██  █▪██▌·██ ▐███▪    ▐█ ▀ ▪▀▄.▀·•█▌▐█
█▌·.█▌█▌▐█▌▄█▀▀█ ▐█▐▐▌ ▐█.▪█▌▐█▌▐█ ▌▐▌▐█·    ▄█ ▀█▄▐▀▀▪▄▐█▐▐▌
▐█▪▄█·▐█▄█▌▐█▪ ▐▌██▐█▌ ▐█▌·▐█▄█▌██ ██▌▐█▌    ▐█▄▪▐█▐█▄▄▌██▐█▌
·▀▀█.  ▀▀▀  ▀  ▀ ▀▀ █▪ ▀▀▀  ▀▀▀ ▀▀  █▪▀▀▀    ·▀▀▀▀  ▀▀▀ ▀▀ █▪
-------------------------------------------------------------
""")

free_gen_channel = 1152488451254538288, 1156430240038526990, 1156701943809454161  # Channel ID here
keep_alive()

free_cooldowns = {}

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents, help_command=None)
intents.typing = True

server_name = "GeniXperts"  # Replace with your server name
server_logo = "https://cdn.discordapp.com/attachments/1152488450130452497/1152939469784227963/Adobe_Express_20230917_0452580_1.png"
services = {
    "discord": {
        "ext": "txt",
        "display_name": "Discord",
        "username_label": "Username",
        "password_label": "Password"
    },
    "twitch": {
        "ext": "txt",
        "display_name": "Twitch",
        "username_label": "Username",
        "password_label": "Password"
    },
      "roblox": {
        "ext": "txt",
        "display_name": "Roblox",
        "username_label": "Username",
        "password_label": "Password"
    },
    # Add more services here with their extensions, display names, username, and password labels
}



import os
import nextcord
import asyncio

def get_stock_left():
    stock_count = 0
    for filename in os.listdir("freestock/"):
        with open(f"freestock/{filename}") as f:
            stock_count += len(f.read().splitlines())
    return stock_count

@bot.event
async def on_ready():
    await update_status()  # Set the initial status
    print("Running")

async def update_status():
    swap_flag = False  # Initialize a flag to swap between member count and stock count
    while True:
        # Calculate the total number of members across all servers
        total_member_count = sum([guild.member_count for guild in bot.guilds])

        # Get the current stock count
        stock_left = get_stock_left()

        # Update the bot's status to display either member count or stock count based on the swap_flag
        if swap_flag:
            await bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.watching,
                    name=f"{stock_left} Stock left"
                )
            )
        else:
            await bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.watching,
                    name=f"{total_member_count} Members"
                )
            )

        # Toggle the swap_flag for the next update
        swap_flag = not swap_flag

        await asyncio.sleep(10)  # Update status every 30 seconds

# Define a cooldown dictionary to keep track of users and their cooldowns
gen_cooldowns = {}

# Function to check if a user is blacklisted
def is_user_blacklisted(user_id):
    try:
        with open("blacklist.txt", "r") as blacklist_file:
            blacklist = blacklist_file.read().splitlines()
            return str(user_id) in blacklist
    except FileNotFoundError:
        return False  # Return False if the blacklist file doesn't exist

# Modify the gen command to include the blacklist check and cooldown
@bot.slash_command(name="gen", description="Generate free accounts (Discord, Twitch, Roblox, and more)")
async def gen(inter, service):
    user = inter.user
    user_id = inter.user.id

    # Check if the user is on the blacklist
    if is_user_blacklisted(user_id):
        await inter.send("You are blacklisted and cannot use this command.", ephemeral=True)
        return

    # Check if the command is used in one of the specified channels
    allowed_channels = (1152488451254538288, 1156430240038526990, 1156701943809454161)
    if inter.channel.id not in allowed_channels:
        embed = nextcord.Embed(
            title="Wrong Channel!",
            description="Please use this command in one of the specified channels.",
            color=nextcord.Color.red()
        )
        await inter.send(embed=embed, ephemeral=True)
        return
      
    service = service.lower()
    if service not in services:
        available_services = ", ".join(services.keys())
        embed = nextcord.Embed(title="Invalid Service!",
                               description=f"Available services: {available_services}",
                               color=nextcord.Color.red())
        await inter.send(embed=embed, ephemeral=True)
        return

    service_details = services[service]
    stock_file = f"{service}.{service_details['ext']}"

    if stock_file not in os.listdir("freestock//"):
        embed = nextcord.Embed(title=f"The stock for {service_details['display_name']} is not available.",
                               color=nextcord.Color.red())
        await inter.send(embed=embed, ephemeral=True)
        return

    # Check if the user is on cooldown
    if user_id in gen_cooldowns and time.time() - gen_cooldowns[user_id] < 1200:
        cooldown_time = int(1200 - (time.time() - gen_cooldowns[user_id]))
        minutes, seconds = divmod(cooldown_time, 60)
        await inter.send(f"You can use this command again in {minutes} minutes and {seconds} seconds.", ephemeral=True)
        return

    with open(f"freestock//{stock_file}") as file:
        lines = file.read().splitlines()
        if len(lines) == 0:
            embed = nextcord.Embed(title=f"Out of stock for {service_details['display_name']}!",
                                   description="Please wait until we restock.",
                                   color=nextcord.Color.red())
            out_of_stock_msg = await inter.send(embed=embed, ephemeral=True)

            # Delete the "Out of stock" message after 30 seconds
            await asyncio.sleep(30)
            await out_of_stock_msg.delete()

            return

    account = random.choice(lines)
    combo = account.split('|')  # Change the delimiter to "|"

    if len(combo) < 2:  # Check if there are at least 2 elements in the combo list
        embed = nextcord.Embed(title="Account Format Error", description="The account format is not as expected.",
                               color=nextcord.Color.red())
        await inter.send(embed=embed, ephemeral=True)
        return

    username_label = service_details['username_label']
    password_label = service_details['password_label']

    User = combo[0]
    Pass = combo[1]
    Password = Pass.rstrip()

    embed = nextcord.Embed(title=server_name, color=nextcord.Color.yellow())
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    embed.add_field(name=f"Service Type:", value=f"```{service_details['display_name']}```")
    embed.add_field(name=f"{username_label}:", value=f"```{str(User)}```")
    embed.add_field(name=f"{password_label}:", value=f"```{str(Password)}```")

    # Send the account information as a DM to the user
    await user.send(embed=embed)

    name = (stock_file[0].upper() + stock_file[1:].lower()).replace(".txt", "")

    embed1 = nextcord.Embed(title=f"{name} Account Generated!", description="> Check your DMs for your account!",
                            color=nextcord.Color.green())
    embed1.set_footer(text=server_name, icon_url=server_logo)
    embed1.set_thumbnail(url=server_logo)
    out_of_stock_msg = await inter.send(embed=embed1)

    # Remove the account from the current stock file
    lines.remove(account)
    with open(f"freestock//{stock_file}", "w", encoding='utf-8') as file:
        file.write("\n".join(lines))

    # Set user cooldown
    gen_cooldowns[user_id] = time.time()

    # Delete the "Out of stock" message after 30 seconds
    await asyncio.sleep(30)
    await out_of_stock_msg.delete()


@bot.slash_command(name="stock", description="View free stock!")
async def freestock(inter: nextcord.Interaction):
    embed = nextcord.Embed(title="Account Stock", color=nextcord.Color.green(),
                           timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    embed.description = ""
    for filename in os.listdir("freestock/"):
        with open(f"freestock/{filename}") as f:
            amount = len(f.read().splitlines())
            name = (filename[0].upper() + filename[1:].lower()).replace(".txt", "")
            embed.description += f"* **{name}**: `{amount}`\n"
    await inter.send(embed=embed, ephemeral=True)

@bot.slash_command(name="help", description="Show all available commands!")
async def help(ctx):
    embed = nextcord.Embed(title=server_name, color=nextcord.Color.red())
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    embed.add_field(name="/help", value="Shows this command", inline=False)
    embed.add_field(name="/gen", value="Generate free accounts", inline=False)
    embed.add_field(name="/stock", value="View free stock", inline=False)
    embed.add_field(name="/feedback", value="Give feedback on the bot", inline=False)
    embed.add_field(name="/mygenhistory", value="View your generation history", inline=False)

    await ctx.send(embed=embed)

# Define the allowed user ID
allowed_user_id = 1147153683742724147

@bot.slash_command(
    name="addaccount",
    description="Add an account to the stock (Bot only)",
)
async def add_account(ctx: nextcord.Interaction, service: str, account_info: str):
    # Check if the command is invoked by the allowed user
    if ctx.user.id != 1153437951192203305:
        await ctx.send("This command is only available to the specified user.")
        return

    # Check if the specified service is valid
    service = service.lower()
    if service not in services:
        available_services = ", ".join(services.keys())
        await ctx.send(f"Invalid Service! Available services: {available_services}")
        return

    # Determine the filename for the service
    service_details = services[service]
    stock_file = f"freestock/{service}.{service_details['ext']}"

    # Append the account information to the service-specific file
    with open(stock_file, "a", encoding='utf-8') as file:
        file.write(account_info + "\n")

    # After adding the account, you can send a confirmation message.
    await ctx.send(f"Account for {service} added to the stock.")

    # You should also update the stock count and potentially handle any other logic here.

# Function to get a user's generation history (replace with your actual implementation)
def get_user_gen_history(user_id):
    # Implement your logic to fetch the user's generation history here
    # Return a list of dictionaries, each containing service, date, and result
    # Example: history = [{"service": "Discord", "date": "2023-09-17", "result": "Success"}]
    return []

@bot.slash_command(name="mygenhistory", description="View your generation history")
async def mygenhistory(ctx: nextcord.Interaction):
    # Implement the logic to retrieve and display the user's generation history here
    # You can use ctx.user.id to identify the user and fetch their history

    # Example: Fetch user's history (replace this with your actual logic)
    user_id = ctx.user.id
    history = get_user_gen_history(user_id)  # Implement this function to retrieve user history

    if history:
        # Create and send an embed or message to display the user's history
        embed = nextcord.Embed(title="Your Generation History", color=nextcord.Color.blue())
        embed.set_footer(text=server_name, icon_url=server_logo)
        embed.set_thumbnail(url=server_logo)

        for entry in history:
            # Add each entry to the embed
            embed.add_field(name="Service", value=entry["service"], inline=True)
            embed.add_field(name="Date", value=entry["date"], inline=True)
            embed.add_field(name="Result", value=entry["result"], inline=False)

        await ctx.send(embed=embed, ephemeral=True)
    else:
        await ctx.send("It seems you have no History if you think this is a glitch contact us.", ephemeral=True)



@bot.slash_command(name="feedback", description="Submit feedback about the bot")
async def feedback_command(ctx: nextcord.Interaction):
    # Inform the user that a DM will be sent
    await ctx.send("I will send you a DM to collect your feedback.", ephemeral=True)

    # Send a prompt to the user in DMs
    try:
        # Create an embed message to collect feedback
        feedback_embed = nextcord.Embed(
            title="Give Your Feedback",
            description="Please provide your feedback below. Type 'cancel' to cancel the feedback submission.",
            color=nextcord.Color.green()
        )
        feedback_embed.set_footer(text="Bot Feedback")

        await ctx.user.send(embed=feedback_embed)
    except nextcord.Forbidden:
        await ctx.send("I couldn't send you a DM. Please make sure your DMs are open and try again.", ephemeral=True)
        return

    try:
        # Wait for the user's response in DMs
        def check_dm(message):
            return message.author == ctx.user and message.channel == ctx.user.dm_channel

        response = await bot.wait_for("message", check=check_dm, timeout=300)  # Adjust the timeout as needed

        # Check if the user canceled the feedback submission
        if response.content.lower() == "cancel":
            await ctx.user.send("Feedback submission canceled.")
            return

        # Collect the user's feedback
        feedback = response.content

        # Define the path to the feedback.txt file (relative to your project)
        feedback_file_path = "feedback.txt"  # Adjust the path as needed

        # Write the feedback to the feedback.txt file
        with open(feedback_file_path, "a", encoding="utf-8") as feedback_file:
            feedback_file.write(f"User {ctx.user.name} (ID: {ctx.user.id}) submitted feedback:\n")
            feedback_file.write(f"{feedback}\n\n")

        # Send a confirmation message to the user in DMs
        await ctx.user.send("Thank you for your feedback! It has been received and will be reviewed.")

    except asyncio.TimeoutError:
        # Handle the case where the user didn't respond within the timeout
        await ctx.user.send("You didn't provide feedback within the time limit. Please use /feedback again if needed.")

    except Exception as e:
        # Handle any other errors that may occur
        print(f"An error occurred while processing feedback: {str(e)}")
        await ctx.user.send("An error occurred while processing your feedback. Please try again later.")











@bot.slash_command(name="credits", description="View the credits for this server.")
async def credits(ctx):
    # Fetch server information dynamically
    server_name = ctx.guild.name
    server_logo = ctx.guild.icon.url

    # Create an embed with customizable color
    embed = nextcord.Embed(title=f"Credits for {server_name}", color=0x3498db)
    embed.set_thumbnail(url=server_logo)

    # Define credits information with names and roles (mentionable)
    credits_info = [
        ("Owner", ctx.guild.owner.mention),
        ("Developed by", "Moobe, Ys.Nesa"),
        ("Restockers", "Cipher, Nesa, Brooklyn"),
        ("Contributors", "Sizl, Guve, Maxwell"),
        ("Special Thanks", "EZA CODING, RTX CODING, Uptimerobot"),
        # Add more categories and contributors as needed
    ]

    for field_name, field_value in credits_info:
        embed.add_field(name=field_name, value=field_value, inline=False)

    # Add clickable links (if applicable)
    # Example: ("GitHub", "[GitHub](https://github.com/user)")

    # Include a footer with a message or additional information
    embed.set_footer(text="Thank you to all our amazing contributors!")

    # Send the embed
    await ctx.send(embed=embed)
    
    # Check if ctx.message exists before trying to delete it
    if ctx.message:
        await asyncio.sleep(5)
        await ctx.message.delete()












# Import necessary modules and functions
import nextcord

import nextcord

import datetime
import asyncio
import nextcord

@bot.slash_command(name="restockinfo", description="Information about account restocking")
async def restock_info(ctx):
    # Define the restocking schedule
    schedule = [
        {"day": "Monday", "accounts": 5},
        {"day": "Tuesday", "accounts": 0},
        {"day": "Wednesday", "accounts": 3},
        {"day": "Thursday", "accounts": 0},
        {"day": "Friday", "accounts": 5},
        {"day": "Saturday", "accounts": 0},
        {"day": "Sunday", "accounts": 3},
    ]

    # Create an embed message
    embed = nextcord.Embed(
        title="Restocking Schedule (Checkmark means current day)",
        color=nextcord.Color.green()
    )

    # Get the current day of the week
    current_day = datetime.datetime.now().strftime("%A")

    # Build the restocking schedule in the embed
    for entry in schedule:
        day = entry["day"]
        accounts = entry["accounts"]

        # Use a checkmark emoji if it's today's date, otherwise, leave it empty
        emoji = "✅" if day == current_day else "❌"

        # Add the day and account information to the schedule
        embed.add_field(
            name=f"{emoji} {day}",
            value=f"Accounts: {accounts}",
            inline=True
        )

    # Send the embed message as a response
    message = await ctx.send(embed=embed, ephemeral=True)

    # Delete the message after 30 seconds
    await asyncio.sleep(30)
    await message.delete()


# Rest of your code ...

# ... (Rest of your code, including other commands/functions and bot initialization) ...

# Run the bot
bot.run(os.environ["token"])


import nextcord

@bot.event
async def on_member_join(member):
    # This event is triggered when a member joins the server

    # Replace '1155243230451994696' with the ID of your target channel
    channel_id = 1155243230451994696
    welcome_channel = bot.get_channel(channel_id)

    if welcome_channel:
        embed = discord.Embed(
            title=f'Welcome to the server, {member.display_name}!',
            description="We're excited to have you here.",
            color=0x00ff00  # You can customize the color here
        )
        embed.add_field(name="Rules", value="Please review the server rules in the 📋・rules channel.")
        embed.add_field(name="Get Started", value="Get started by verifying in the ☑・verify channel.")
        embed.set_thumbnail(url=member.avatar_url)

        await welcome_channel.send(embed=embed)









@bot.event
async def on_member_remove(member):
    # Replace this with the action you want to perform when a member leaves
    # For example, you can send a farewell message in a specific channel
    farewell_channel_id = 1155337754754945024 # Replace with the actual channel ID
    
    # Get the farewell channel
    farewell_channel = member.guild.get_channel(farewell_channel_id)
    if farewell_channel:
        # Create an embedded farewell message
        embed = nextcord.Embed(
            title=f"Goodbye, {member.display_name}!",
            description="We'll miss you hope you enjoyed our gen.",
            color=nextcord.Color.red()  # You can customize the color here
        )
        
        # Use member's avatar URL (use default avatar if no custom avatar)
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        embed.set_thumbnail(url=avatar_url)
        
        # Send the farewell message as an embedded message
        await farewell_channel.send(embed=embed)




@bot.event
async def on_message(message):
    # Check if the message is in the target channel and not sent by the specified user
    if message.channel.id == 1152488451254538288 and message.author.id != 1153437951192203305:
        # Wait for 30 seconds
        await asyncio.sleep(5)
        # Delete the message
        await message.delete()

@bot.event
async def on_message(message):
    # Check if the message is in the target channel and is sent by the bot itself
    if message.channel.id == 1152488451254538288 and message.author.id == bot.user.id:
        # Wait for 5 seconds
        await asyncio.sleep(5)
        # Delete the message
        await message.delete()



# Your existing code ...





















# The rest of your code remains unchanged

# ... (rest of your code)

bot.run(os.environ["token"])
