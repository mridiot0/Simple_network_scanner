## Network Scanner

This Python script is a simple network scanner that allows users to discover devices on a network and scan open ports on a specific device.

### Features:
- **Device Discovery:** Users can scan a network range to discover devices and their corresponding MAC addresses.
- **Port Scanning:** Users can scan for open ports on a specified device within a network range.
- **Port Scan Options:** Supports scanning the top 100 ports, top 1000 ports, or a custom range of ports.
- **Output to File:** Results of the port scan are saved to a text file (**Live**), allowing users to review the findings later.

### Usage:
1. Run the script and choose the desired option from the main menu.
2. Input the necessary parameters, such as network range or host IP, depending on the chosen option.
3. View the scan results on the console and find detailed results saved in a text file with a timestamped filename.

### Dependencies:
- [`scapy`](https://pypi.org/project/scapy/): For crafting and sending packets on the network. Install via pip: `pip install scapy`
- [`colorama`](https://pypi.org/project/colorama/): For adding color and style to console output. Install via pip: `pip install colorama`

### Note:
- Ensure proper permissions and dependencies are installed before running the script.
- This script is for educational and informational purposes only. Use responsibly and respect the privacy and security of network devices.
