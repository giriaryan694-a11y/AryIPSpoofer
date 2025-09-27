#!/usr/bin/env python3
import socket
import select
import threading
import struct
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
    print(colored("--- IP Spoofer + SOCKS5 Proxy ---", "yellow"))
    print(colored("Made By Aryan Giri\n", "light_magenta"))

# Spoof a test packet (UDP/ICMP)
def spoof_test_packet(spoof_ip, protocol="icmp", interface="eth0"):
    try:
        if protocol.lower() == "udp":
            packet = IP(src=spoof_ip, dst="8.8.8.8") / UDP(dport=53) / "Spoofed UDP Packet"
        elif protocol.lower() == "icmp":
            packet = IP(src=spoof_ip, dst="8.8.8.8") / ICMP() / "Spoofed ICMP Packet"
        else:
            print(colored("[!] Only UDP/ICMP supported for spoofing.", "red"))
            return
        send(packet, iface=interface, verbose=False)
        print(colored(f"[+] Sent spoofed {protocol.upper()} test packet from {spoof_ip} to 8.8.8.8", "green"))
    except Exception as e:
        print(colored(f"[!] Spoofing failed: {e}", "red"))

# Custom SOCKS5 Proxy Server
class ArySOCKS5Proxy:
    def __init__(self, spoof_ip, proxy_port, username=None, password=None):
        self.spoof_ip = spoof_ip
        self.proxy_port = proxy_port
        self.username = username
        self.password = password
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", proxy_port))
        self.server_socket.listen(5)
        print(colored(f"[+] SOCKS5 Proxy running on 0.0.0.0:{proxy_port} (Spoofed IP: {spoof_ip})", "green"))
        if username and password:
            print(colored(f"[+] Auth enabled: Username={username}", "green"))

    def socks5_handshake(self, client_socket):
        try:
            # Read client greeting
            greeting = client_socket.recv(2)
            if not greeting or len(greeting) != 2:
                return False
            version, nmethods = greeting
            if version != 5:
                return False
            methods = client_socket.recv(nmethods)
            if 0 not in methods and 2 not in methods:  # No auth or user/pass auth
                return False
            # Send server choice
            if 2 in methods and self.username and self.password:
                client_socket.sendall(b"\x05\x02")  # Require user/pass auth
                # Handle user/pass auth
                version = client_socket.recv(1)
                if version != b"\x01":
                    return False
                username_len = ord(client_socket.recv(1))
                username = client_socket.recv(username_len)
                password_len = ord(client_socket.recv(1))
                password = client_socket.recv(password_len)
                if username != self.username.encode() or password != self.password.encode():
                    client_socket.sendall(b"\x01\x01")  # Auth failed
                    return False
                client_socket.sendall(b"\x01\x00")  # Auth success
            else:
                client_socket.sendall(b"\x05\x00")  # No auth required
            return True
        except Exception as e:
            print(colored(f"[!] Handshake error: {e}", "red"))
            return False

    def handle_client(self, client_socket):
        try:
            if not self.socks5_handshake(client_socket):
                client_socket.close()
                return

            # Read client request
            header = client_socket.recv(4)
            if len(header) < 4:
                client_socket.close()
                return
            version, cmd, _, address_type = header

            # Parse address
            if address_type == 1:  # IPv4
                address = socket.inet_ntoa(client_socket.recv(4))
            elif address_type == 3:  # Domain
                domain_len = ord(client_socket.recv(1))
                address = client_socket.recv(domain_len).decode()
            else:
                client_socket.close()
                return

            port = struct.unpack(">H", client_socket.recv(2))[0]

            # Connect to target
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((address, port))
            bind_response = b"\x05\x00\x00\x01" + socket.inet_aton("0.0.0.0") + struct.pack(">H", 2222)
            client_socket.sendall(bind_response)

            # Relay traffic
            sockets = [client_socket, remote_socket]
            while True:
                readable, _, _ = select.select(sockets, [], [])
                for sock in readable:
                    try:
                        data = sock.recv(4096)
                        if not data:
                            return
                        if sock is client_socket:
                            remote_socket.sendall(data)
                        else:
                            client_socket.sendall(data)
                    except Exception as e:
                        return
        except Exception as e:
            print(colored(f"[!] Proxy error: {e}", "red"))
        finally:
            client_socket.close()
            if 'remote_socket' in locals():
                remote_socket.close()

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(colored(f"[+] New connection from {addr}", "blue"))
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

# Input-based menu
def get_user_input():
    print_banner()
    spoof_ip = input(colored("[?] Enter IP to spoof: ", "yellow"))
    protocol = input(colored("[?] Enter protocol for test packet (icmp/udp): ", "yellow")).lower()
    interface = input(colored("[?] Enter network interface (e.g., eth0): ", "yellow")) or "eth0"

    # SOCKS5 options
    use_auth = input(colored("[?] Use username/password for SOCKS5? (y/n): ", "yellow")).lower() == "y"
    username, password = None, None
    if use_auth:
        username = input(colored("[?] Enter SOCKS5 username: ", "yellow"))
        password = input(colored("[?] Enter SOCKS5 password: ", "yellow"))
    proxy_port = int(input(colored("[?] Enter SOCKS5 proxy port (default 1080): ", "yellow")) or 1080)

    return {
        "spoof_ip": spoof_ip,
        "protocol": protocol,
        "interface": interface,
        "use_auth": use_auth,
        "username": username,
        "password": password,
        "proxy_port": proxy_port,
    }

# Main
def main():
    config = get_user_input()

    # Spoof a test packet
    spoof_test_packet(
        spoof_ip=config["spoof_ip"],
        protocol=config["protocol"],
        interface=config["interface"],
    )

    # Start SOCKS5 proxy in a thread
    proxy = ArySOCKS5Proxy(
        spoof_ip=config["spoof_ip"],
        proxy_port=config["proxy_port"],
        username=config["username"],
        password=config["password"],
    )
    proxy_thread = threading.Thread(target=proxy.start)
    proxy_thread.daemon = True
    proxy_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print(colored("\n[!] Exiting...", "yellow"))

if __name__ == "__main__":
    main()
