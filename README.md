# 💻 Wake Panel – Remote Power Control via WOL & ESP32 Relay

## 🌐 Project Description

**Wake Panel** is a Flask-based web application that lets you remotely power on computers using Wake-on-LAN (WOL) or an ESP32-driven relay. Perfect for home labs, server farms, or IoT setups where you need a single, unified interface to manage multiple machines.

---

## 🚀 Features

- **Web Dashboard**: Secure login, add/remove hosts, view real-time status (On/Off/Maintenance/Error).  
- **WOL Support**: Send “magic packets” to NICs with WOL enabled.  
- **ESP32 Relay Mode**: Trigger a physical relay via ESP32 HTTP POST for machines without WOL.  
- **Multi-host Management**: Store host IPs, MACs, and ESP32 addresses in `pcs.json`.  
- **SSH & Ping Health Checks**: Auto-detect host state via ping and optional SSH test.  
- **Internationalized Docs**: Separate `en/` and `es/` folders for English and Spanish deployment.

---

## 🎯 Requirements

### Hardware
- A server or SBC (e.g., Raspberry Pi, Atom Lite) running your Flask app  
- Target PCs with WOL-capable NICs  
- ESP32 (or similar) + relay module for non-WOL machines  

### Software
- Python 3.8+  
- Flask  
- `python-pam` (for PAM authentication)  
- Paramiko (for SSH testing)  
- `ethtool` (for persistent WOL on Linux)  
- `curl` (for ESP32 HTTP calls)

---

## 🔧 Hardware Setup

1. **WOL-Enabled Machine**  
   - In BIOS: enable **Power On by Onboard LAN** and disable **ErP/Deep Power Off**.  
   - On Linux:
     ```bash
     sudo ethtool enp0s25 wol g
     ```

2. **ESP32 Relay Machine**  
   - Wire relay COM/NO across the PC’s front-panel power switch pins.  
   - Power the relay module (5 V) from ESP32 VIN/GND (or external 5 V supply).  
   - Control the relay input from an ESP32 GPIO pin (e.g., GPIO 26).

---

## 🛠️ Hardware Installation & Software Installation

```bash
ESP32 Config
# Download the INO file and compile it for your ESP32
# Edit the file with your WiFi credentials and the correct pin configuration

BIOS Config (WOL)
# Enter BIOS -> Advanced or Power section
# Enable “Power On by Onboard LAN” or similar
# Disable ErP/Deep Power Off (otherwise the network card will be off)

---

# Clone repository
git clone https://github.com/oscarnadals/wakeonlan.git
cd wake-panel

# Create & activate virtual environment (non-mandatory)
python3 -m venv venv
source venv/bin/activate

# (Recommended) Use screen or tmux to keep the Flask server running after SSH disconnects:
screen -S wake-panel

# Install Python dependencies
pip install Flask python-pam paramiko

# Install system tools (Debian/Ubuntu)
sudo apt update
sudo apt install ethtool curl

# Run the Flask app
python3 app.py
