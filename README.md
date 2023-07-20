# vCenter Insight Discord Bot

![Python](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9-blue)
![Discord.py](https://img.shields.io/badge/discord.py-1.7.3-blue)

The vCenter Insight Discord Bot is a Python-based bot that connects to a vCenter server and reports on active VMs within specific folders. It utilizes the Discord.py library for Discord integration and the pyVmomi library for vCenter server communication.

## Features

- Connects to a Discord server and listens for commands.
- Connects to a vCenter server using provided credentials.
- Reports active VMs within a specified folder on the Discord channel.

## Requirements

- Python 3.7, 3.8, or 3.9
- Discord.py 1.7.3
- pyVmomi

## Setup

1. Clone the repository to your local machine.

2. Install the required dependencies:
    - pip install discord.py
    - pip install pyvmomi


3. Set up your Discord bot:

- Create a Discord account if you don't have one.
- Go to the Discord Developer Portal (https://discord.com/developers/applications) and create a new application to get your bot token.
- Replace `YOUR_DISCORD_BOT_TOKEN` with your actual bot token in the `vcenter_bot.py` file.

4. Set up your vCenter server:

- Provide your vCenter server URL, username, and password in the `vcenter_url`, `vcenter_username`, and `vcenter_password` variables in the `vcenter_bot.py` file.

## Usage

1. Run the bot:
python vcenter_bot.py


2. Invite the bot to your Discord server using the generated OAuth2 URL from the Discord Developer Portal.

3. Use the `!reportVMs` command in any channel where the bot is present to get a list of active VMs within the specified folder.

## Note

Please ensure that the bot has sufficient permissions to access the Discord server and the vCenter server.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The [Discord.py](https://github.com/Rapptz/discord.py) library for Discord integration.
- The [pyVmomi](https://github.com/vmware/pyvmomi) library for vCenter server communication.

Feel free to contribute, report issues, or suggest improvements by creating an issue or pull request!
