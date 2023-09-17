import nextcord
import os
import random
import datetime
import asyncio
import typing
from nextcord.ext import commands
from keep_alive import keep_alive

free_gen_channel = 1152488451254538288  # Channel ID here
keep_alive()

free_cooldowns = {}

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents, help_command=None)
intents.typing = True

server_name = "GeniXperts"  # Replace with your server name
server_logo = "https://cdn.discordapp.com/attachments/1152488450130452497/1152939469784227963/Adobe_Express_20230917_0452580_1.png"

# Define services and their details (extension, display name, username label, password label)
services = {
    "discord": {"ext": "txt", "display_name": "Discord", "username_label": "Username", "password_label": "Password"},
    "twitch": {"ext": "txt", "display_name": "Twitch", "username_label": "Username", "password_label": "Password"},
    "roblox": {"ext": "txt", "display_name": "Roblox", "username_label": "Username", "password_label": "Password"},
    "minecraft": {"ext": "txt", "display_name": "Minecraft", "username_label": "Username", "password_label": "Password"},
    "netflix": {"ext": "txt", "display_name": "Netflix", "username_label": "Email", "password_label": "Password"},
    "epicgames": {"ext": "txt", "display_name": "Epic Games", "username_label": "Username", "password_label": "Password"},
    # Add more services here with their extensions, display names, username, and password labels
}

# Implement a function to calculate stock left based on your data
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
    while True:
        stock_left = get_stock_left()
        await bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.watching,
                name=f"{stock_left} Stock left"
            )
        )
        await asyncio.sleep(3.0)  # Update status every 1 hour

@bot.slash_command(name="gen", description="Generate free accounts (Discord, Twitch, Roblox, and more)")
async def gen(inter, service):
    user = inter.user
    user_id = inter.user.id

    if user_id in free_cooldowns:
        remaining_cooldown = free_cooldowns[user_id]
        hours = remaining_cooldown // 3600
        minutes = (remaining_cooldown % 3600) // 60
        seconds = remaining_cooldown % 60

        cooldown_message = (
            f"**Command Cooldown:** You can use this command again in "
            f"{hours} hours, {minutes} minutes, and {seconds} seconds."
        )

        embed = nextcord.Embed(
            title="Cooldown",
            description=cooldown_message,
            color=nextcord.Color.red(),
        )
        await inter.send(embed=embed, ephemeral=True)
        return

    if inter.channel.id != free_gen_channel:
        embed = nextcord.Embed(title="Wrong Channel! Use <#free_gen_channel>", color=nextcord.Color.red())
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

    with open(f"freestock//{stock_file}") as file:
        lines = file.read().splitlines()
        if len(lines) == 0:
            embed = nextcord.Embed(title=f"Out of stock for {service_details['display_name']}!",
                                   description="Please wait until we restock.",
                                   color=nextcord.Color.red())
            await inter.send(embed=embed, ephemeral=True)
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
    await user.send(embed=embed)

    name = (stock_file[0].upper() + stock_file[1:].lower()).replace(".txt", "")

    embed1 = nextcord.Embed(title=f"{name} Account Generated!", description="> Check your DMs for your account!",
                            color=nextcord.Color.green())
    embed1.set_footer(text=server_name, icon_url=server_logo)
    embed1.set_thumbnail(url=server_logo)
    await inter.send(embed=embed1)

    # Remove the account from the current stock file
    lines.remove(account)
    with open(f"freestock//{stock_file}", "w", encoding='utf-8') as file:
        file.write("\n".join(lines))

    free_cooldowns[user_id] = 3600  # 1 hour cooldown

    async def cooldown_task():
        await asyncio.sleep(3600)  # Sleep for 1 hour
        del free_cooldowns[user_id]
    bot.loop.create_task(cooldown_task())

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

    await ctx.send(embed=embed)



# Define the allowed user ID
allowed_user_id = 1147153683742724147

@bot.slash_command(
    name="addaccount",
    description="Add an account to the stock (Bot only)",
)
async def add_account(ctx: nextcord.Interaction, service: str, account_info: str):
    # Check if the command is invoked by the allowed user
    if ctx.user.id != allowed_user_id:
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

# Your existing code ...

# The rest of your code remains unchanged



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













bot.run(os.environ["token"])
