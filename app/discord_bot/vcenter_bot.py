import discord
import ssl
import os
from discord.ext import commands
from dotenv import load_dotenv
from pyVim.connect import SmartConnect, Disconnect, vim

# Load the environment vars from the .env file
load_dotenv()

# Discord bot token
discord_token = os.getenv('discord_token')

# vCenter server details
vcenter_url = 'https://vcenter.thouse.lab'
vcenter_username = os.getenv('vcenter_username')
vcenter_password = os.getenv('vcenter_password')

class MyClient(discord.Client):
    async def on_ready(self):
        print("Successfully logged in as: ", self.user)
    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith(('/reportVMs')):
            await reportVMs(message)

async def reportVMs(message):
    try:
        # Connect to the vCenter server
        s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        s.verify_mode = ssl.CERT_NONE
        vcenter_instance = SmartConnect(host=vcenter_url, user=vcenter_username, pwd=vcenter_password, sslContext=s)

        # Get VMs in a specific folder
        folder_path = '/THOUSE/vm/GeekWerkesLab/'
        active_vms = get_active_vms_in_folders(vcenter_instance, folder_path)

        # Disconnect from the vCenter server
        Disconnect(vcenter_instance)

        # Report active VMs on Discord
        if active_vms:
            report_message = "\n".join(active_vms)
            await message.channel.send(f"Active VMs in specific folder {folder_path}:\n{report_message}")
        else:
            await message.channel.send(f"No active VMs found in folder {folder_path}.")
    except Exception as e:
        await message.channel.send(f"Error: {str(e)}")

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

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)