# AryIPSpoofer

**AryIPSpoofer** is a Python tool for sending spoofed IP packets (UDP/ICMP). It allows you to craft packets with a spoofed source IP address.

---

## 📌 Features
- **IP Spoofing**: Craft and send spoofed UDP/ICMP packets
- **User-Friendly**: Input-based menu for easy configuration
- **Banner**: Decorative ASCII art with "Made By Aryan Giri"

---

## 🛠 Setup

### 1. Clone the Repository
```bash
git clone https://github.com/giriaryan694-a11y/AryIPSpoofer.git
cd AryIPSpoofer
```
### 2. Install Dependencies
```
pip install -r requirements.txt --break-system-packages
```
> **Note:** Use a virtual environment if preferred:

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Run the Tool
```
sudo python3 ary_ipspoofer.py
```
> **Note:** Root privileges are required for raw packet operations.

## 🚀 Usage
**Configure the Tool**
Follow the prompts to:

1. Enter the source IP to spoof
2. Enter the destination IP
3. Choose protocol (udp/icmp)
4. Enter destination port (for UDP)
5. Enter network interface (default: eth0)

## ⚠️ Important Notes
• Sends individual spoofed UDP/ICMP packets using Scapy
• For educational purposes in controlled environments

### Legal and Ethical Considerations
• Use Responsibly: Only in networks where you have explicit permission
• Legal Risks: Unauthorized spoofing is illegal in most jurisdictions
• Network Limitations: Most networks filter spoofed packets

