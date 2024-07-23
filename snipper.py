import paramiko
import argparse
from authentication import UsernamePasswordAuthentication, UsernamePrivateKeyAuthentication
from getpass import getpass


class Snipper:
    """A ninja in the shadows, a sniper in the distance—where stealth meets precision, mastery is born."""

    def __init__(self, host, port, auth):
        self.host = host
        self.port = port
        self.auth = auth

    def scan_ports(self, target_ip, ports):
        """Scan ports on a target IP via SSH."""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Authenticate using the provided authentication class
            self.auth.authenticate(self.host, self.port, ssh)

            # Prepare the Nmap command
            port_list = ','.join(map(str, ports))
            nmap_command = f'nmap -p {port_list} {target_ip}'

            # Execute the Nmap command
            stdin, stdout, stderr = ssh.exec_command(nmap_command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            # Parse the output
            open_ports = []
            closed_ports = []

            if error:
                print(f"Error executing Nmap command: {error}")
                return open_ports, closed_ports

            for line in output.splitlines():
                # print(line)
                if 'open' in line:
                    parts = line.split()
                    port = parts[0].split('/')[0]
                    open_ports.append(port)
                elif 'closed' in line:
                    parts = line.split()
                    port = parts[0].split('/')[0]
                    closed_ports.append(port)

            return open_ports, closed_ports

        except paramiko.SSHException as e:
            print(f"SSH connection failed: {e}")
            return [], []

        finally:
            ssh.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scan ports on a target IP via SSH.')
    parser.add_argument('--host', required=True, help='SSH server hostname or IP address')
    parser.add_argument('--port', type=int, default=22, help='SSH server port (default: 22)')
    parser.add_argument('--username', required=True, help='SSH username')
    parser.add_argument('--password', action='store_true', help='SSH password (if using password authentication)')
    parser.add_argument('--private-key', help='Path to SSH private key file or key string')
    parser.add_argument('--key-type', choices=['RSA', 'ECDSA', 'Ed25519'], help='Type of private key')
    parser.add_argument('--target-ip', required=True, help='Target IP address for port scanning')
    parser.add_argument('--ports', nargs='+', type=int, required=True, help='Ports to scan (space-separated)')

    args = parser.parse_args()

    if not args.password and not args.private_key:
        print("Error: Either --password or --private-key must be provided.")
        parser.print_help()
        exit(1)

    if args.private_key:
        auth = UsernamePrivateKeyAuthentication(
            username=args.username,
            private_key=args.private_key,
            key_type=args.key_type
        )
    else:
        password = getpass(f"Password for user {args.username}: ")
        auth = UsernamePasswordAuthentication(username=args.username, password=password)

    snipper = Snipper(host=args.host, port=args.port, auth=auth)
    open_ports, closed_ports = snipper.scan_ports(target_ip=args.target_ip, ports=args.ports)

    print("Open Ports:", open_ports)
    print("Closed Ports:", closed_ports)
