import nextcord
import os
import random
import datetime
import asyncio
import typing
from nextcord.ext import commands
from keep_alive import keep_alive
import time

print("""
.▄▄▄  ▄• ▄▌ ▄▄▄·  ▐ ▄ ▄▄▄▄▄▄• ▄▌• ▌ ▄ ·.      ▄▄ • ▄▄▄ . ▐ ▄ 
▐▀•▀█ █▪██▌▐█ ▀█ •█▌▐█•██  █▪██▌·██ ▐███▪    ▐█ ▀ ▪▀▄.▀·•█▌▐█
█▌·.█▌█▌▐█▌▄█▀▀█ ▐█▐▐▌ ▐█.▪█▌▐█▌▐█ ▌▐▌▐█·    ▄█ ▀█▄▐▀▀▪▄▐█▐▐▌
▐█▪▄█·▐█▄█▌▐█▪ ▐▌██▐█▌ ▐█▌·▐█▄█▌██ ██▌▐█▌    ▐█▄▪▐█▐█▄▄▌██▐█▌
·▀▀█.  ▀▀▀  ▀  ▀ ▀▀ █▪ ▀▀▀  ▀▀▀ ▀▀  █▪▀▀▀    ·▀▀▀▀  ▀▀▀ ▀▀ █▪
-------------------------------------------------------------
""")

free_gen_channel = 1238964613714808853, 1156430240038526990, 1156701943809454161, 1158976650311127081
keep_alive()

free_cooldowns = {}

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents, help_command=None)
intents.typing = True

server_name = "Art Generator"
server_logo = "https://github.com/DamageCoding/doxedkids/blob/main/SImpleytlogo%20(1).png?raw=true"
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
    "steam": {
        "ext": "txt",
        "display_name": "Steam",
        "username_label": "Username",
        "password_label": "Password"
    },
}

def get_stock_left():
    stock_count = 0
    for filename in os.listdir("freestock/"):
        with open(f"freestock/{filename}") as f:
            stock_count += len(f.read().splitlines())
    return stock_count

@bot.event
async def on_ready():
    await update_status()
    print("Running")

async def update_status():
    swap_flag = False
    while True:
        total_member_count = sum([guild.member_count for guild in bot.guilds])
        stock_left = get_stock_left()

        if swap_flag:
            await bot.change_presence(
                activity=nextcord.Activity(type=nextcord.ActivityType.watching,
                                           name=f"{stock_left} Stock left"))
        else:
            await bot.change_presence(activity=nextcord.Activity(
                type=nextcord.ActivityType.watching,
                name=f"{total_member_count} Members"))

        swap_flag = not swap_flag
        await asyncio.sleep(10)

gen_cooldowns = {}

def is_user_blacklisted(user_id):
    try:
        with open("blacklist.txt", "r") as blacklist_file:
            blacklist = blacklist_file.read().splitlines()
            return str(user_id) in blacklist
    except FileNotFoundError:
        return False

@bot.slash_command(
    name="gen",
    description="Generate free accounts (Discord, Twitch, Roblox, and more)")
async def gen(inter, service):
    user = inter.user
    user_id = inter.user.id

    if is_user_blacklisted(user_id):
        await inter.send("You are blacklisted and cannot use this command.",
                         ephemeral=True)
        return

    allowed_channels = [1238964613714808853]
    if inter.channel.id not in allowed_channels:
        embed = nextcord.Embed(
            title="Wrong Channel!",
            description=
            "Please use this command in one of the specified channels.",
            color=nextcord.Color.red())
        await inter.send(embed=embed, ephemeral=True)
        return

    service = service.lower()
    if service not in services:
        available_services = ", ".join(services.keys())
        embed = nextcord.Embed(
            title="Invalid Service!",
            description=f"Available services: {available_services}",
            color=nextcord.Color.red())
        await inter.send(embed=embed, ephemeral=True)
        return

    service_details = services[service]
    stock_file = f"{service}.{service_details['ext']}"

    if stock_file not in os.listdir("freestock//"):
        embed = nextcord.Embed(
            title=
            f"The stock for {service_details['display_name']} is not available.",
            color=nextcord.Color.red())
        await inter.send(embed=embed, ephemeral=True)
        return

    if user_id in gen_cooldowns and time.time(
    ) - gen_cooldowns[user_id] < 1200:
        cooldown_time = int(1200 - (time.time() - gen_cooldowns[user_id]))
        minutes, seconds = divmod(cooldown_time, 60)
        await inter.send(
            f"You can use this command again in {minutes} minutes and {seconds} seconds.",
            ephemeral=True)
        return

    with open(f"freestock//{stock_file}") as file:
        lines = file.read().splitlines()
        if len(lines) == 0:
            embed = nextcord.Embed(
                title=f"Out of stock for {service_details['display_name']}!",
                description="Please wait until we restock.",
                color=nextcord.Color.red())
            out_of_stock_msg = await inter.send(embed=embed, ephemeral=True)

            await asyncio.sleep(30)
            await out_of_stock_msg.delete()
            return

    account = random.choice(lines)
    combo = account.split('|')

    if len(combo) < 2:
        embed = nextcord.Embed(
            title="Account Format Error",
            description="The account format is not as expected.",
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
    embed.add_field(name=f"Service Type:",
                    value=f"```{service_details['display_name']}```")
    embed.add_field(name=f"{username_label}:", value=f"```{str(User)}```")
    embed.add_field(name=f"{password_label}:", value=f"```{str(Password)}```")

    await user.send(embed=embed)

    name = (stock_file[0].upper() + stock_file[1:].lower()).replace(".txt", "")

    embed1 = nextcord.Embed(title=f"{name} Account Generated!",
                            description="> Check your DMs for your account!",
                            color=nextcord.Color.green())
    embed1.set_footer(text=server_name, icon_url=server_logo)
    embed1.set_thumbnail(url=server_logo)
    out_of_stock_msg = await inter.send(embed=embed1)

    lines.remove(account)
    with open(f"freestock//{stock_file}", "w", encoding='utf-8') as file:
        file.write("\n".join(lines))

    gen_cooldowns[user_id] = time.time()

    log_embed = nextcord.Embed(title="Account Generation Log",
                               color=nextcord.Color.green())
    log_embed.add_field(name="User", value=f"{user.mention}", inline=False)
    log_embed.add_field(name="Service",
                        value=f"{service_details['display_name']}",
                        inline=False)
    log_embed.add_field(name=f"{username_label}:",
                        value=f"{User}",
                        inline=True)
    log_embed.add_field(name=f"{password_label}:",
                        value=f"{Password}",
                        inline=True)

    log_channel_id = 1238958686295031850
    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send(embed=log_embed)

    await asyncio.sleep(30)
    await out_of_stock_msg.delete()

@bot.slash_command(name="stock", description="View free stock!")
async def freestock(inter: nextcord.Interaction):
    embed = nextcord.Embed(title="Account Stock",
                           color=nextcord.Color.green(),
                           timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    embed.description = ""
    for filename in os.listdir("freestock/"):
        with open(f"freestock/{filename}") as f:
            amount = len(f.read().splitlines())
            name = (filename[0].upper() + filename[1:].lower()).replace(
                ".txt", "")
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
    embed.add_field(name="/feedback",
                    value="Give feedback on the bot",
                    inline=False)
    embed.add_field(name="/mygenhistory",
                    value="View your generation history",
                    inline=False)

    await ctx.send(embed=embed)

allowed_user_id = 1147153683742724147

@bot.slash_command(
    name="addaccount",
    description="Add an account to the stock (Bot only)",
)
async def add_account(ctx: nextcord.Interaction, service: str,
                      account_info: str):
    if ctx.user.id != 1153437951192203305:
        await ctx.send("This command is only available to the specified user.")
        return

    service = service.lower()
    if service not in services:
        available_services = ", ".join(services.keys())
        await ctx.send(
            f"Invalid Service! Available services: {available_services}")
        return

    service_details = services[service]
    stock_file = f"freestock/{service}.{service_details['ext']}"

    with open(stock_file, "a", encoding='utf-8') as file:
        file.write(account_info + "\n")

    await ctx.send(f"Account for {service} added to the stock.")

def get_user_gen_history(user_id):
    return []

@bot.slash_command(name="mygenhistory",
                   description="View your generation history")
async def mygenhistory(ctx: nextcord.Interaction):
    user_id = ctx.user.id
    history = get_user_gen_history(user_id)

    if history:
        embed = nextcord.Embed(title="Your Generation History",
                               color=nextcord.Color.blue())
        embed.set_footer(text=server_name, icon_url=server_logo)
        embed.set_thumbnail(url=server_logo)

        for entry in history:
            embed.add_field(name="Service",
                            value=entry["service"],
                            inline=True)
            embed.add_field(name="Date", value=entry["date"], inline=True)
            embed.add_field(name="Result", value=entry["result"], inline=False)

        await ctx.send(embed=embed, ephemeral=True)
    else:
        await ctx.send(
            "It seems you have no History if you think this is a glitch contact us.",
            ephemeral=True)

@bot.slash_command(name="feedback",
                   description="Submit feedback about the bot")
async def feedback_command(ctx: nextcord.Interaction):
    await ctx.send("I will send you a DM to collect your feedback.",
                   ephemeral=True)

    try:
        feedback_embed = nextcord.Embed(
            title="Give Your Feedback",
            description=
            "Please provide your feedback below. Type 'cancel' to cancel the feedback submission.",
            color=nextcord.Color.green())
        feedback_embed.set_footer(text="Bot Feedback")

        await ctx.user.send(embed=feedback_embed)
    except nextcord.Forbidden:
        await ctx.send(
            "I couldn't send you a DM. Please make sure your DMs are open and try again.",
            ephemeral=True)
        return

    try:
        def check_dm(message):
            return message.author == ctx.user and message.channel == ctx.user.dm_channel

        response = await bot.wait_for("message", check=check_dm, timeout=300)

        if response.content.lower() == "cancel":
            await ctx.user.send("Feedback submission canceled.")
            return

        feedback = response.content
        feedback_file_path = "feedback.txt"

        with open(feedback_file_path, "a", encoding="utf-8") as feedback_file:
            feedback_file.write(
                f"User {ctx.user.name} (ID: {ctx.user.id}) submitted feedback:\n"
            )
            feedback_file.write(f"{feedback}\n\n")

        await ctx.user.send(
            "Thank you for your feedback! It has been received and will be reviewed."
        )

    except asyncio.TimeoutError:
        await ctx.user.send(
            "You didn't provide feedback within the time limit. Please use /feedback again if needed."
        )

    except Exception as e:
        print(f"An error occurred while processing feedback: {str(e)}")
        await ctx.user.send(
            "An error occurred while processing your feedback. Please try again later."
        )

@bot.slash_command(name="credits",
                   description="View the credits for this server.")
async def credits(ctx):
    server_name = ctx.guild.name
    server_logo = ctx.guild.icon.url

    embed = nextcord.Embed(title=f"Credits for {server_name}", color=0x3498db)
    embed.set_thumbnail(url=server_logo)

    credits_info = [
        ("Owner", ctx.guild.owner.mention),
        ("Developed by", "Moobe, Ys.Nesa"),
        ("Restockers", "Cipher, Nesa, Brooklyn"),
        ("Contributors", "Sizl, Guve, Maxwell"),
        ("Special Thanks", "EZA CODING, RTX CODING, Uptimerobot"),
    ]

    for field_name, field_value in credits_info:
        embed.add_field(name=field_name, value=field_value, inline=False)

    embed.set_footer(text="Thank you to all our amazing contributors!")

    await ctx.send(embed=embed)

    if ctx.message:
        await asyncio.sleep(5)
        await ctx.message.delete()

@bot.slash_command(name="restockinfo",
                   description="Information about account restocking")
async def restock_info(ctx):
    schedule = [
        {
            "day": "Monday",
            "accounts": 5
        },
        {
            "day": "Tuesday",
            "accounts": 0
        },
        {
            "day": "Wednesday",
            "accounts": 3
        },
        {
            "day": "Thursday",
            "accounts": 0
        },
        {
            "day": "Friday",
            "accounts": 5
        },
        {
            "day": "Saturday",
            "accounts": 0
        },
        {
            "day": "Sunday",
            "accounts": 3
        },
    ]

    embed = nextcord.Embed(
        title="Restocking Schedule (Checkmark means current day)",
        color=nextcord.Color.green())

    current_day = datetime.datetime.now().strftime("%A")

    for entry in schedule:
        day = entry["day"]
        accounts = entry["accounts"]

        emoji = "✅" if day == current_day else "❌"

        embed.add_field(name=f"{emoji} {day}",
                        value=f"Accounts: {accounts}",
                        inline=True)

    message = await ctx.send(embed=embed, ephemeral=True)

    await asyncio.sleep(30)
    await message.delete()

@bot.slash_command(
    name="getuserids",
    description="Get and save all user IDs and usernames in a server")
async def get_user_ids(ctx: nextcord.Interaction):
    if ctx.user.guild_permissions.administrator:
        members = ctx.guild.members

        user_info = [
            f"{member.id}: {member.display_name}" for member in members
        ]

        with open("id.txt", "w") as id_file:
            id_file.write("\n".join(user_info))

        await ctx.send("User IDs and usernames have been saved to id.txt.",
                       ephemeral=True)
    else:
        await ctx.send(
            "This command is only available to users with administrative permissions.",
            ephemeral=True)

@bot.slash_command(name="blacklist", description="Add a user to the blacklist")
async def blacklist_user(ctx: nextcord.Interaction, user: nextcord.User):
    if ctx.user.guild_permissions.administrator:
        user_id = user.id

        with open("blacklist.txt", "r") as blacklist_file:
            blacklisted_ids = blacklist_file.read().splitlines()

        if str(user_id) in blacklisted_ids:
            await ctx.send(f"{user.mention} is already blacklisted.",
                           ephemeral=True)
        else:
            with open("blacklist.txt", "a") as blacklist_file:
                blacklist_file.write(str(user_id) + "\n")

            await ctx.send(f"{user.mention} has been blacklisted.",
                           ephemeral=True)
    else:
        await ctx.send(
            "This command is only available to users with administrative permissions.",
            ephemeral=True)

@bot.slash_command(name="unblacklist",
                   description="Remove a user from the blacklist")
async def unblacklist_user(ctx: nextcord.Interaction, user: nextcord.User):
    if ctx.user.guild_permissions.administrator:
        user_id = user.id

        with open("blacklist.txt", "r") as blacklist_file:
            blacklisted_ids = blacklist_file.read().splitlines()

        if str(user_id) in blacklisted_ids:
            blacklisted_ids.remove(str(user_id))

            with open("blacklist.txt", "w") as blacklist_file:
                blacklist_file.write("\n".join(blacklisted_ids))

            await ctx.send(
                f"{user.mention} has been removed from the blacklist.",
                ephemeral=True)
        else:
            await ctx.send(f"{user.mention} is not in the blacklist.",
                           ephemeral=True)
    else:
        await ctx.send(
            "This command is only available to users with administrative permissions.",
            ephemeral=True)

@bot.slash_command(name="ban", description="Ban a user from the server")
async def ban_user(ctx: nextcord.Interaction, user: nextcord.User):
    if ctx.user.guild_permissions.administrator:
        try:
            await ctx.guild.ban(user, reason="Banned by command")
            await ctx.send(f"{user.mention} has been banned.", ephemeral=True)
        except nextcord.errors.NotFound:
            await ctx.send("User not found.", ephemeral=True)
    else:
        await ctx.send(
            "This command is only available to users with administrative permissions.",
            ephemeral=True)

@bot.slash_command(name="announce",
                   description="Announce a message with optional @everyone")
async def announce(ctx: nextcord.Interaction,
                   message: str,
                   ping_everyone: bool = False,
                   channel: nextcord.TextChannel = None):
    if ctx.user.id == 1122571804729421986:
        if channel is None:
            channel = ctx.channel

        if ping_everyone:
            announcement = f"@everyone {message}"
        else:
            announcement = message

        await channel.send(announcement)

        await ctx.send(f"Announcement sent to {channel.mention}: {message}")
    else:
        await ctx.send("This command is only available to a specific user.")

@bot.slash_command(
    name="genrequest",
    description="Request a specific service for account generation.")
async def request_service(ctx: nextcord.Interaction, service: str):
    user_id = ctx.user.id
    user_display_name = ctx.user.display_name

    request_message = f"User ID: {user_id}\nUser Display Name: {user_display_name}\nRequested Service: {service}\n\n"

    with open("servicerequest.txt", "a") as request_file:
        request_file.write(request_message)

    await ctx.send(
        f"Your request for {service} has been received and recorded. Thank you for your suggestion!",
        ephemeral=True)

bot.run(os.environ["token"])

import keep_alive

keep_alive.keep_alive()
