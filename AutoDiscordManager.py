from time import sleep
import psutil
from scapy.all import ARP, Ether, srp
import subprocess

# Constants
ARP_TIMEOUT = 3
CHECK_INTERVAL = 5
MAX_CHECKS = 3
DEVICE_IP = '192.168.1.24'  # Replace with the IP address of the device you want to monitor
DISCORD_FILE_PATH = 'C:\\Users\\Alecv\\AppData\\Local\\Discord\\app-1.0.9032\\Discord.exe'  # Replace with the file path of Discord on your system

def get_mac(ip):
    """
    Get the MAC address of a given IP address using ARP.

    Args:
        ip (str): The IP address to get the MAC address for.

    Returns:
        str: The MAC address of the given IP address.
    """
    # Create an ARP request packet
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # Send the packet and receive the response
    result = srp(packet, timeout=ARP_TIMEOUT, verbose=0)[0]

    # Extract the MAC address from the response
    return result[0][1].hwsrc

def check_device_status(device_ip):
    """
    Check the status of a device by its IP address.

    Args:
        device_ip (str): The IP address of the device.

    Returns:
        bool: True if the device is found, False otherwise.
    """
    try:
        # Get the MAC address of the device
        get_mac(device_ip)
        return True
    except IndexError:
        # Device not found, return False
        return False

def is_discord_open():
    """
    Check if Discord application is currently running.

    Returns:
        bool: True if Discord is running, False otherwise.
    """
    # Iterate over all running processes
    for proc in psutil.process_iter(['name']):
        # Check if the process is Discord.exe
        if proc.info['name'] == 'Discord.exe':
            return True
    return False

def close_discord():
    """
    Closes the Discord application if it is currently running.

    This function iterates over all running processes and checks if the process
    name is 'Discord.exe'. If a running process with the name 'Discord.exe' is found,
    it is terminated.

    Note: This function requires the `psutil` module to be installed.

    Returns:
        None
    """
    # Iterate over all running processes
    for proc in psutil.process_iter(['name']):
        # Check if the process is Discord.exe
        if proc.info['name'] == 'Discord.exe':
            # Kill the process
            proc.kill()

import subprocess

def open_discord(file_path):
    """
    Opens Discord using the subprocess module with the specified file path.

    Parameters:
    file_path (str): The path to the Discord executable file.

    Returns:
    None
    """
    subprocess.Popen(file_path)

def main():
    """
    Main function that continuously checks the device status and closes 
    Discord if the device is not found and opens discord if it is found.
    """
    while True:
        checks = 0
        while checks < MAX_CHECKS:
            sleep(CHECK_INTERVAL)
            if not check_device_status(DEVICE_IP):
                # Device not found, increment the number of checks
                checks += 1
                if checks == MAX_CHECKS:
                    # If the device is still not found after MAX_CHECKS, close Discord
                    close_discord()
            else:
                # Device found, reset the number of checks
                checks = 0
                if not is_discord_open():
                    # If Discord is not open, open it
                    open_discord(DISCORD_FILE_PATH)

if __name__ == "__main__":
    main()