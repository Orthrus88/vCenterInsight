import discord
import ssl
import os
import re
import argparse
from dotenv import load_dotenv
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl, vim

# Load the environment vars from the .env file
load_dotenv()

# Discord bot token
discord_token = os.getenv('discord_token')

# vCenter server details
vcenter_url = 'vcenter.thouse.lab'
vcenter_username = os.getenv('vcenter_username')
vcenter_password = os.getenv('vcenter_password')

def format_vm_info(virtual_machine):
    """
    Format information for a particular virtual machine.
    Returns a formatted string.
    """
    summary = virtual_machine.summary
    info = (
        f"Name       : {summary.config.name}\n"
        f"Template   : {summary.config.template}\n"
        f"Path       : {summary.config.vmPathName}\n"
        f"Guest      : {summary.config.guestFullName}\n"
        f"Instance UUID : {summary.config.instanceUuid}\n"
        f"Bios UUID     : {summary.config.uuid}\n"
        f"State      : {summary.runtime.powerState}\n"
    )
    annotation = summary.config.annotation
    if annotation:
        info += f"Annotation : {annotation}\n"

    if summary.guest is not None:
        ip_address = summary.guest.ipAddress
        tools_version = summary.guest.toolsStatus
        if tools_version is not None:
            info += f"VMware-tools: {tools_version}\n"
        else:
            info += "Vmware-tools: None\n"

        if ip_address:
            info += f"IP         : {ip_address}\n"
        else:
            info += "IP         : None\n"

    if summary.runtime.question is not None:
        info += f"Question  : {summary.runtime.question.text}\n"

    info += "\n"
    return info

class MyClient(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith(('/reportVMs')):
            await reportVMs(message)

async def reportVMs(message):
    # Parse custom arguments for the reportVMs function
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--find', required=False, action='store', help='String to match VM names')
    args = parser.parse_args(message.content.split()[1:])

    # Connect to the vCenter server
    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    s.verify_mode = ssl.CERT_NONE
    vcenter_instance = SmartConnect(host=vcenter_url, user=vcenter_username, pwd=vcenter_password, sslContext=s)

    try:
        content = vcenter_instance.RetrieveContent()

        container = content.rootFolder
        view_type = [vim.VirtualMachine]
        recursive = True
        container_view = content.viewManager.CreateContainerView(container, view_type, recursive)

        children = container_view.view
        if args.find is not None:
            pat = re.compile(args.find, re.IGNORECASE)

        info_message = ""
        for child in children:
            if args.find is None or (args.find is not None and pat.search(child.summary.config.name) is not None):
                info = format_vm_info(child)
                # Check if adding this VM's info will exceed the limit
                if len(info_message) + len(info) <= 1900:
                    info_message += info
                else:
                    await message.channel.send(f"```\n{info_message}```")
                    info_message = info

        # Send the remaining info_message, if any
        if info_message:
            await message.channel.send(f"```\n{info_message}```")

        Disconnect(vcenter_instance)

    except vmodl.MethodFault as error:
        await message.channel.send(f"Caught vmodl fault: {error.msg}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_token)