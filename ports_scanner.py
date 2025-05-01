import socket
import argparse
import sys
import threading
import time
import re

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def is_valid_port(port):
    return port.isdigit() and 1 <= int(port) <= 65535

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  
        result = s.connect_ex((ip, port))
        if result == 0:
            print(f"[+] Port {port} : OPEN")
        else:
            print(f"[-] Port {port} : CLOSED")
    except Exception as err:
        print(f"[!] Error on port {port} : {err}")
    finally:
        s.close()

parser = argparse.ArgumentParser(description='Simple multithreaded port scanner')
parser.add_argument('-t', '--target', required=True, help='Target IP address')
parser.add_argument('-p', '--ports', required=True, help='Comma-separated list of ports to scan')

args = parser.parse_args()

if not is_valid_ip(args.target):
    print("[!] Invalid IP address")
    sys.exit(1)

port_strings = args.ports.split(',')
ports = []
for port_str in port_strings:
    if is_valid_port(port_str):
        ports.append(int(port_str))
    else:
        print(f"[!] Invalid port: {port_str}")
        sys.exit(1)

start_time = time.time()
print(f"[i] Starting scan on {args.target}...")

threads = []
for port in ports:
    thread = threading.Thread(target=scan_port, args=(args.target, port))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end_time = time.time()
duration = end_time - start_time
print(f"\n[i] Scan completed in {duration:.2f} seconds.")
