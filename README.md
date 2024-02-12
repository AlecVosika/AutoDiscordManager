# Device Monitor with Discord Control

This Python application continuously monitors the status of a specified device on the local network and manages the Discord application accordingly. If the device is not found, it closes the Discord application, and if the device is found, it ensures that Discord is running.
## Requirements
- Python 3.x
- `psutil` module
- `scapy` module
## Installation
1. Clone or download the repository containing the source code.
2. Install the required Python modules using pip:
```python
    pip install psutil scapy
```
## Configuration
Before running the application, make sure to configure the following parameters in the config.ini:
- `device_ip`: Replace it with the IP address of the device you want to monitor.
- `discord_file_path`: Replace it with the file path of Discord on your system.
## Usage
### Option 1: Download the current release version
Download the current release version [Here](https://github.com/AlecVosika/AutoDiscordManager/releases/tag/V1.0.0).
Once downloaded, open the *_internal* folder and then edit the *config.ini* file with your own parameters.
### Option 2: Create your own Executable 
1. Clone the repo
2. Edit the config.ini file with your own *device_ip* and *discord_file_path*
3. Run the following in the console
```Python
python -m PyInstaller --onefile --add-data "config.ini;." --noconsole AutoDiscordManager.py
```
You will find a file called AutoDiscordManager.exe in the newly created dist folder
## Description
The application includes the following functions:
- `get_mac(ip)`: Retrieves the MAC address of a given IP address using ARP.
- `check_device_status(device_ip)`: Checks the status of a device by its IP address.
- `is_discord_open()`: Checks if the Discord application is currently running.
- `close_discord()`: Closes the Discord application if it is currently running.
- `open_discord(file_path)`: Opens Discord using the subprocess module with the specified file path.
- `main()`: Main function that continuously checks the device status and manages the Discord application accordingly.
## Note
- This application requires administrative privileges to perform operations such as closing and opening applications.
- Ensure that the necessary modules (`psutil`, `scapy`) are installed before running the application.
## Disclaimer
This application is provided as-is without any warranties. Use it at your own risk.