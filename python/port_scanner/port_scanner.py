import socket


target_ip = "127.0.0.1"
ports = range(1, 1025)


for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target_ip, port))
    if result == 0:
        print(f"Port {port} is OPEN")
    else:
        print(f"Port {port} is CLOSED — code: {result}")
    s.close()

import argparse

parser = argparse.ArgumentParser(description="True's Port Scanner")
parser.add_argument("ip", help="Target IP address")
parser.add_argument("start_port", type=int, help="Start port")
parser.add_argument("end_port", type=int, help="End port")
args = parser.parse_args()
