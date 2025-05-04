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

## 🛠️ Software Installation

```bash
# Clone repository
git clone https://github.com/YourUser/wake-panel.git
cd wake-panel

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install Flask python-pam paramiko

# Install system tools (Debian/Ubuntu)
sudo apt update
sudo apt install ethtool curl
