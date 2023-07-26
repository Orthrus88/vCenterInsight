import ssl
import os
from dotenv import load_dotenv
from pyVim.connect import SmartConnect, Disconnect, vim

load_dotenv()

# vCenter server details
vcenter_url = 'vcenter.thouse.lab'
vcenter_username = os.getenv('vcenter_username')
vcenter_password = os.getenv('vcenter_password')

def print_entity_hierarchy(entity, indent=0):
    """
    Recursively print the entity hierarchy starting from the given entity.

    Args:
        entity: The starting entity.
        indent (int, optional): Indentation level for the entity hierarchy print. Default is 0.
    """
    if isinstance(entity, vim.Datacenter):
        print("  " * indent + entity.__class__.__name__ + ": " + entity.name)
    else:
        print("  " * indent + entity.__class__.__name__ + ": " + entity.name)
        if hasattr(entity, 'childEntity'):
            for child in entity.childEntity:
                print_entity_hierarchy(child, indent + 1)

def main():
    try:
        # Connect to the vCenter server
        s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        s.verify_mode = ssl.CERT_NONE
        vcenter_instance = SmartConnect(host=vcenter_url, user=vcenter_username, pwd=vcenter_password, sslContext=s)

        # Get the root folder
        content = vcenter_instance.RetrieveContent()
        root_folder = content.rootFolder

        # Print the entire hierarchy starting from the root folder
        print("vSphere Folder Structure:")
        print_entity_hierarchy(root_folder)

        # Disconnect from the vCenter server
        Disconnect(vcenter_instance)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()