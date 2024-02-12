import logging
import time 
import psutil
from scapy.all import ARP, Ether, srp
import subprocess
import configparser
import os
import sched

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the absolute path to config.ini
config_path = os.path.join(script_dir, 'config.ini')

config = configparser.ConfigParser()
config.read(config_path)

# Constants
ARP_TIMEOUT = 3
CHECK_INTERVAL = 5
MAX_FAILED_CHECKS = 5
DEVICE_IP = config.get('Device', 'device_ip')
DISCORD_FILE_PATH = config.get('Discord', 'discord_file_path')

class DeviceMonitor:
    """
    A class for monitoring the status of a device.

    Attributes:
        device_ip (str): The IP address of the device to monitor.
        discord_file_path (str): The file path of the Discord file.

    Methods:
        get_mac(ip): Get the MAC address of a given IP address using ARP.
        check_device_status(): Check the status of a device by its IP address.
    """

    def __init__(self, device_ip, discord_file_path):
        self.device_ip = device_ip
        self.discord_file_path = discord_file_path

    def get_mac(self, ip):
        """
        Get the MAC address of a given IP address using ARP.

        Args:
            ip (str): The IP address to get the MAC address for.

        Returns:
            str: The MAC address of the given IP address.
        """
        arp = ARP(pdst=ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, timeout=ARP_TIMEOUT, verbose=0)[0]
        return result[0][1].hwsrc

    def check_device_status(self):
            """
            Checks the status of a device by retrieving its MAC address using the device's IP address.

            Returns:
                bool: True if the device is found and its MAC address is retrieved successfully, False otherwise.
            """
            try:
                self.get_mac(self.device_ip)
                return True
            except IndexError:
                logging.error(f"Device with IP {self.device_ip} not found.")
                return False
            except Exception as e:
                logging.error(f"An error occurred while checking device status: {str(e)}")
                return False

class DiscordController:
    """
    A class that provides methods to interact with Discord application.
    """

    @staticmethod
    def is_discord_open():
        """
        Check if Discord application is currently open.

        Returns:
            bool: True if Discord is open, False otherwise.
        """
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'Discord.exe':
                return True
        return False

    @staticmethod
    def close_discord():
        """
        Close the Discord application if it is currently open.
        """
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'Discord.exe':
                proc.kill()

    @staticmethod
    def open_discord(file_path):
        """
        Open the Discord application using the specified file path.

        Args:
            file_path (str): The path to the Discord executable file.
        """
        subprocess.Popen(file_path)

def monitor_and_control(device_monitor, discord_controller, scheduler, failed_checks=0):
    """
    Monitors the device status using the device_monitor, controls Discord using the discord_controller,
    and schedules the next check using the scheduler.

    Args:
        device_monitor: An object that provides methods to check the device status.
        discord_controller: An object that provides methods to control Discord.
        scheduler: An object that provides scheduling functionality.
        failed_checks: The number of consecutive failed checks.

    Returns:
        None
    """
    # Check the device status
    if not device_monitor.check_device_status():
        failed_checks += 1
        # If consecutive failed checks exceed the maximum allowed, close Discord
        if failed_checks >= MAX_FAILED_CHECKS:
            discord_controller.close_discord()
            failed_checks = 0
        # Schedule the next check
        scheduler.enter(CHECK_INTERVAL, 1, monitor_and_control, 
                        (device_monitor, discord_controller, scheduler, failed_checks))
        return

    failed_checks = 0

    # If Discord is not open, open Discord
    if not discord_controller.is_discord_open():
        discord_controller.open_discord(DISCORD_FILE_PATH)

    # Schedule the next check
    scheduler.enter(CHECK_INTERVAL, 1, monitor_and_control, 
                    (device_monitor, discord_controller, scheduler, failed_checks))



def main():
    """
    Entry point of the program.
    Initializes the device monitor, discord controller, and scheduler.
    Schedules the initial monitoring and control task.
    """
    device_monitor = DeviceMonitor(DEVICE_IP, DISCORD_FILE_PATH)
    discord_controller = DiscordController()
    scheduler = sched.scheduler(time.time, time.sleep)

    # Schedule the initial monitoring and control task
    scheduler.enter(0, 1, monitor_and_control, 
                    (device_monitor, discord_controller, scheduler))
    scheduler.run()

if __name__ == "__main__":
    main()
