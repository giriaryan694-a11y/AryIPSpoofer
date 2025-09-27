# AryIPSpoofer

**AryIPSpoofer** is a Python tool for IP spoofing and SOCKS5 proxy routing. It allows you to spoof your IP address for outgoing packets and route traffic from other tools through a SOCKS5 proxy, optionally protected with a username and password.

---

## 📌 Features
- **IP Spoofing**: Spoof your IP for UDP/ICMP packets.
- **SOCKS5 Proxy**: Route traffic from other tools through a spoofed IP.
- **Optional Authentication**: Secure your proxy with a username and password.
- **User-Friendly**: Input-based menu for easy configuration.
- **Banner**: Decorative ASCII art banner with "Made By Aryan Giri".

---

## 🛠 Setup

### 1. Clone the Repository
```bash
git clone https://github.com/giriaryan694-a11y/AryIPSpoofer.git

cd AryIPSpoofer
```
### 2. Install Dependencies

```
python -m venv aryipspoofer
source aryipspoofer/bin/activate
pip3 install -r requirements.txt

```
> OR
```
pip3 install -r requirements.txt --break-system-packages
```

### 3. Run the Tool

```
sudo python main.py
```

> Note: Root privileges are required for raw socket operations.

## 🚀 Usage

### 1. Configure the Tool
**Follow the prompts to:**

• Enter the IP to spoof.
• Choose the protocol for the test packet (UDP/ICMP).
• Enter the network interface (e.g., eth0).
• Optionally, enable authentication for the SOCKS5 proxy.

### 2. Use the SOCKS5 Proxy
**Once the proxy is running, you can route traffic from other tools through it:**
```
curl --socks5 127.0.0.1:1080 http://example.com
```
**Replace 1080 with the port you configured.**

##⚠️ Legal and Ethical Notes

• **Use Responsibly**: This tool is for **educational and authorized testing purposes only.**
• **Unauthorized Use**: Spoofing IP addresses without permission is **illegal** in most jurisdictions.
• **Network Restrictions**: Spoofing may not work on networks with ingress filtering.

This project is for **educational purposes only.** Use at your own risk.


