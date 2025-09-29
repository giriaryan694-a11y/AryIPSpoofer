#!/usr/bin/env python3
from scapy.all import IP, UDP, ICMP, send
import pyfiglet
from termcolor import colored
from colorama import init

# Initialize colorama
init()

# Banner
def print_banner():
    banner = pyfiglet.figlet_format("AryIPSpoofer", font="slant")
    print(colored(banner, "cyan"))
    print(colored("--- IP Spoofer by Aryan Giri ---", "yellow"))
    print(colored("Made By Aryan Giri\n", "light_magenta"))

def spoof_packet(src_ip, dst_ip, dst_port, protocol="icmp", interface="eth0"):
    try:
        if protocol.lower() == "udp":
            packet = IP(src=src_ip, dst=dst_ip) / UDP(dport=dst_port) / "Spoofed UDP Packet"
        elif protocol.lower() == "icmp":
            packet = IP(src=src_ip, dst=dst_ip) / ICMP() / "Spoofed ICMP Packet"
        else:
            print(colored("[!] Only UDP/ICMP supported for spoofing.", "red"))
            return
        send(packet, iface=interface, verbose=False)
        print(colored(f"[+] Sent spoofed {protocol.upper()} packet from {src_ip} to {dst_ip}", "green"))
    except Exception as e:
        print(colored(f"[!] Spoofing failed: {e}", "red"))

def get_user_input():
    print_banner()
    src_ip = input(colored("[?] Enter source IP to spoof: ", "yellow"))
    dst_ip = input(colored("[?] Enter destination IP: ", "yellow"))
    protocol = input(colored("[?] Enter protocol (udp/icmp): ", "yellow")).lower()
    dst_port = 0
    if protocol == "udp":
        dst_port = int(input(colored("[?] Enter destination port: ", "yellow")) or 0)
    interface = input(colored("[?] Enter network interface (e.g., eth0): ", "yellow")) or "eth0"
    return {"src_ip": src_ip, "dst_ip": dst_ip, "protocol": protocol, "dst_port": dst_port, "interface": interface}

def main():
    config = get_user_input()
    spoof_packet(
        src_ip=config["src_ip"],
        dst_ip=config["dst_ip"],
        dst_port=config["dst_port"],
        protocol=config["protocol"],
        interface=config["interface"],
    )

if __name__ == "__main__":
    main()
    
