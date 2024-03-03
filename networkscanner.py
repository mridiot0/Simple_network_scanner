#!/usr/bin/env python3
import datetime
import os
import signal
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

import pyfiglet
from colorama import Fore, init
from scapy.all import ARP, Ether, srp

# Function to handle Ctrl+C interrupt
def handler(signum, frame):
    print(Fore.RED + "\nExiting..." + Fore.RESET)
    os._exit(1)

signal.signal(signal.SIGINT, handler)

# Function to check if port is open
def is_port_open(host, port):
    """
    Determine whether `host` has the `port` open
    """
    s = socket.socket()
    try:
        s.connect((host, port))
        s.settimeout(0.2)
    except:
        return False
    else:
        return True

# Function to save output to file
def save_output(file_name, content):
    with open(file_name, 'a') as file:
        file.write(content + '\n')

# Function to scan ports from a file
def scan_ports_from_file(host, file_path, file_name):
    try:
        with open(file_path, 'r') as file:
            nmap_top_ports = [int(port.strip()) for port in file.readlines()]

        for port in nmap_top_ports:
            try:
                if is_port_open(host, port):
                    result = f"[+] {host}:{port} is open"
                else:
                    result = f"[!] {host}:{port} is closed"

                print(result)
                save_output(file_name, result)
            except KeyboardInterrupt:
                print(Fore.RED + "\nExiting..." + Fore.RESET)
                sys.exit(0)
    except FileNotFoundError:
        print(Fore.RED + f"File not found: {file_path}" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}" + Fore.RESET)

# Function to scan ports within a specified range
def scan_ports(host, start_port, end_port, file_name):
    print(Fore.GREEN + f"[+] Starting Port Scan on {host}..." + Fore.RESET)
    open_ports = False
    with ThreadPoolExecutor(max_workers=20) as executor:
        try:
            for port in range(start_port, end_port + 1):
                future = executor.submit(is_port_open, host, port)
                if future.result():
                    open_ports = True
                    result = f"[+] {host}:{port} is open"
                else:
                    result = f"[!] {host}:{port} is closed"

                print(result)
                save_output(file_name, result)
        except KeyboardInterrupt:
            print(Fore.RED + "\nPort scanning interrupted by user." + Fore.RESET)
            os._exit(0)
    if not open_ports:
        print(Fore.RED + "No open ports found. Better luck next time!" + Fore.RESET)
# Initialize colorama for colored output
init()

# Print ASCII banner
ascii_banner = pyfiglet.figlet_format("SCANNER BY KK")

# Main menu
while True:
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    print(ascii_banner)
    print("1. Scan for Network Devices")
    print("2. Scan for Ports")
    print("3. Exit")
    answer = input("What do you want to do? (e.g., 1 or 2): ")

    # Network Devices Scanning
    if answer == "1":
        try:
            target_ip = input("Enter the Network Range (e.g., 192.168.1.0/24): ")
            arp = ARP(pdst=target_ip)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp

            result = srp(packet, timeout=3, verbose=0)[0]
            clients = [{'ip': received.psrc, 'mac': received.hwsrc} for sent, received in result]

            print("Available devices in the network:")
            print(Fore.YELLOW + "IP" + " "*18 + "MAC" + Fore.RESET)
            for client in clients:
                print(Fore.YELLOW + f"{client['ip']:16}    {client['mac']}" + Fore.RESET)
        except KeyboardInterrupt:
            print(Fore.RED + "\nExiting..." + Fore.RESET)
            sys.exit(0)

    # Port Scanning
    elif answer == "2":
        host = input("Enter the host IP: ")
        now = datetime.datetime.now()
        date_sec = now.strftime("%Y-%m-%d-%H-%M-%S")
        file_name = f"{host.replace('.', '-')}_scan_ports_{date_sec}.txt"
        print(f"Scanning ports on {host}. Output will be saved to {file_name}.")

        with open(file_name, 'w') as file:
            file.write(f"Port scanning results for {host}:\n")

        print("\nSelect an option:")
        print("1. Top 100 ports")
        print("2. Top 1000 ports")
        print("3. Custom ports")
        options = input("Enter your choice (1/2/3): ")

        if options == "1":
            top_100_ports = list(range(7, 10)) + [13] + list(range(21, 27)) + [37, 53] + list(range(79, 82)) + [88, 106] + list(range(110, 112)) + [113, 119, 135, 139] + list(range(143, 145)) + [179, 199, 389, 427, 443, 444, 445, 465] + list(range(513, 516)) + list(range(543, 545)) + [548, 554, 587, 631, 646, 873, 990, 993, 995] + list(range(1025, 1030)) + [1110, 1433, 1720, 1723, 1755, 1900] + list(range(2000, 2002)) + [2049, 2121, 2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631, 5666, 5800, 5900] + list(range(6000, 6002)) + [6646, 7070, 8000, 8008, 8009, 8080, 8081, 8443, 8888, 9100] + list(range(9999, 10001)) + [32768] + list(range(49152, 49158))

            for port in top_100_ports:
                try:
                    if is_port_open(host, port):
                        result = f"[+] {host}:{port} is open"
                    else:
                        result = f"[!] {host}:{port} is closed"

                    print(result)
                    save_output(file_name, result)
                except KeyboardInterrupt:
                    print(Fore.RED + "\nExiting..." + Fore.RESET)
                    sys.exit(0)

        elif options == "2":
            file_path = input("Enter the path to the file containing port numbers: ")
            scan_ports_from_file(host, file_path, file_name)

        else:
            try:
                start_port = int(input("Enter the starting port: "))
                end_port = int(input("Enter the ending port: "))
                print("Press Ctrl+C to stop the port scan.")
                scan_ports(host, start_port, end_port, file_name)
            except KeyboardInterrupt:
                print(Fore.RED + "\nExiting..." + Fore.RESET)
                sys.exit(0)

    elif answer == "3":
        print("Exiting...")
        sys.exit(0)

    else:
        print(Fore.RED + "Invalid option. Please try again." + Fore.RESET)
    
    input("\nPress Enter to continue...")
