# Snipper

## Overview

**Snipper** is a powerful Python tool that combines the stealth of a ninja with the precision of a sniper. This tool allows you to perform Nmap scans on specified TCP/UDP ports from a remote server via SSH, providing an efficient way to check if ports are open or closed.

## Features

- **SSH Authentication**: Supports both username/password and username/private key authentication methods.
- **Nmap Integration**: Executes Nmap commands on remote servers to scan specified ports.
- **Port Status Detection**: Returns lists of open and closed ports after scanning.
- **Flexible Authentication**: Handles private keys from files or string variables.
- **Class-Based Structure**: Organized with clear, reusable classes for authentication and SSH operations.

## Requirements

- Python 3.x
- `paramiko` library
- `argparse` library

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/GluGluGlu/Snipper.git
   ```
2. Navigate to the project directory:
   ```sh
   cd snipper
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the script with the required arguments:

### Example with Username and Password

```sh
python snipper.py --host your.ssh.server.com --port 22 --username your_username --password --target-ip 1.1.1.1 --ports 22 80 8443
```

### Example with Private  Key

```sh
python snipper.py --host your.ssh.server.com --port 22 --username your_username --private-key /path/to/your/private_key --key-type RSA --target-ip 1.1.1.1 --ports 22 80 8443
```

## Command-Line Arguments

- `--host`: SSH server hostname or IP address (required)
- `--port`: SSH server port (default: 22)
- `--username`: SSH username (required)
- `--password`: SSH password (if using password authentication)
- `--private-key`: Path to SSH private key file or key string (if using private key authentication)
- `--key-type`: Type of private key (required if using --private-key)
- `--target-ip`: Target IP address for port scanning (required)
- `--ports`: Space-separated list of ports to scan (required)

## Project Structure

- `snipper.py`: Main script file containing the core functionality.
- `README.md`: Project documentation file.

---

Inspired by the precision of snipers and the stealth of ninjas, Snipper aims to provide a seamless and efficient port scanning experience.

---

*"A ninja in the shadows, a sniper in the distance—where stealth meets precision, mastery is born."*

---



