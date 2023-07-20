import discord
import ssl
from discord.ext import commands
from pyVim.connect import SmartConnect, Disconnect, vim

# Discord bot token
discord_bot_token = ''

# vCenter server details
vcenter_url = 'YOUR_VCENTER_SERVER_URL'
vcenter_username = 'YOUR_VCENTER_USERNAME'
vcenter_password = 'YOUR_VCENTER_PASSWORD'

# Discord intents setup
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

# Discord bot setup
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

async def reportVMs(ctx):
    try:
        # Connect to the vCenter server
        s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        s.verify_mode = ssl.CERT_NONE
        vcenter_instance = SmartConnect(host=vcenter_url, user=vcenter_username, pwd=vcenter_password, ssl=s)

        # Get VMs in specific folder
        folder_path = '/THOUSE/GeekWerkesLab/'
        active_vms = get_active_vms_in_folders(vcenter_instance, folder_path)

        # Disconnect from the vCenter server
        Disconnect(vcenter_instance)

        # Report active VMs on Discord
        if active_vms:
            report_message = "\n".join(active_vms)
            await ctx.send(f"Active VMs in specific folder {folder_path}:\n{report_message}")
        else:
            await ctx.send(f"No active VMs found in folder {folder_path}.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

def get_active_vms_in_folders(vcenter_instance, folder_path):
    active_vms = []
    
    # Get the root folder
    content = vcenter_instance.RetrieveContent()
    root_folder = content.rootFolder
    
    # Find the target folder by traversing the inventory tree
    folder = None
    for datacenter in root_folder.childEntity:
        if hasattr(datacenter, 'vmFolder'):
            # Recursively search for the folder path
            folder = find_folder(datacenter.vmFolder, folder_path)
            if folder:
                break

    if folder:
        # Get the list of VMs in the folder
        vm_list = folder.childEntity
        for vm in vm_list:
            if isinstance(vm, vim.VirtualMachine) and vm.runtime.powerState == "poweredOn":
                active_vms.append(vm.name)

    return active_vms

def find_folder(folder, folder_path):
    # Traverse the folder tree to find the target folder
    if folder_path[0] == folder.name:
        if len(folder_path) == 1:
            return folder
        for child in folder.childEntity:
            if hasattr(child, 'childEntity'):
                return find_folder(child, folder_path[1:])
    return None

# Run the Discord bot
bot.run(discord_bot_token)