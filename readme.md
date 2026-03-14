# Discord Account Generator Bot

## ⚠️ DISCLAIMER
**This project hasn't been actively maintained or worked on since 2023. It may contain bugs, deprecated Discord API features, or security issues. Use at your own risk!**

A Discord bot designed for generating and managing free accounts for various services including Discord, Twitch, Roblox, and Steam.

## 📋 Features

- Account generation for multiple services
- Stock management system
- User cooldowns
- Blacklist system
- Feedback collection
- Generation logging
- Admin commands for moderation
- Automatic status updates (member count/stock count)
- Service request system

## 🚀 Commands

### User Commands

| Command | Description |
|---------|-------------|
| /help | Shows all available commands |
| /gen <service> | Generate a free account (services: discord, twitch, roblox, steam) |
| /stock | View available stock for all services |
| /feedback | Submit feedback about the bot |
| /mygenhistory | View your generation history |
| /credits | View server credits |
| /restockinfo | Check the restocking schedule |
| /genrequest <service> | Request a new service to be added |

### Admin Commands

| Command | Description |
|---------|-------------|
| /addaccount <service> <account_info> | Add accounts to stock (format: username\|password) |
| /blacklist <user> | Add a user to the blacklist |
| /unblacklist <user> | Remove a user from the blacklist |
| /ban <user> | Ban a user from the server |
| /announce <message> [ping_everyone] [channel] | Make an announcement |
| /getuserids | Export all user IDs and usernames |

## 🔧 Setup

### Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Required Python packages (see requirements.txt)

### Installation

1. Clone the repository

git clone https://github.com/yourusername/discord-account-generator.git
cd discord-account-generator

2. Install dependencies

pip install nextcord python-dotenv

3. Create a `.env` file or set environment variable

token=YOUR_BOT_TOKEN_HERE

4. Create necessary directories

mkdir freestock

5. Configure channel IDs in the code:
   - free_gen_channel - Channel IDs where gen command can be used
   - log_channel_id - Channel for generation logs
   - allowed_user_id - User ID for admin commands

### File Structure

├── freestock/           # Account files (service.txt)
├── blacklist.txt        # Blacklisted user IDs
├── feedback.txt         # User feedback storage
├── servicerequest.txt   # Service requests
├── id.txt              # Exported user IDs
└── main.py             # Main bot file

### Account File Format

Account files should be placed in the `freestock/` directory with the naming convention: `service.txt`

Format for account entries:

username|password
username|password

Example (discord.txt):

john_doe|password123
jane_smith|securepass456

## ⚙️ Configuration

### Adding New Services

Edit the `services` dictionary in the code:

services = {
    "servicename": {
        "ext": "txt",
        "display_name": "Display Name",
        "username_label": "Username",
        "password_label": "Password"
    },
}

### Changing Cooldowns

Modify the cooldown time in the gen command:

if user_id in gen_cooldowns and time.time() - gen_cooldowns[user_id] < 1200:  # 1200 seconds = 20 minutes

## 🐛 Known Issues

- Some Discord API features may be deprecated
- Cooldown system might not persist through bot restarts
- File-based storage may have race conditions
- Limited error handling in some commands
- No database integration (uses flat files)

## ⚠️ Warning

This bot was created for educational purposes and hasn't been updated since 2023. It may:
- Violate Discord's Terms of Service
- Have security vulnerabilities
- Not work with current Discord API versions
- Contain bugs and stability issues

**Use this code as a reference only. For production use, consider rewriting it with current best practices and security measures.**

## 📝 License

This project is for educational purposes only. Use at your own risk.

## 🤝 Contributing

Since this project is no longer actively maintained, contributions are not being accepted. Feel free to fork the project and maintain your own version.

---

**Last Updated: 2025**
