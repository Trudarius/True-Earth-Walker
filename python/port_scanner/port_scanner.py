import socket
import argparse
import time

parser = argparse.ArgumentParser(description="True's Port Scanner")
parser.add_argument("ip", help="Target IP address")
parser.add_argument("start_port", type=int, help="Start port")
parser.add_argument("end_port", type=int, help="End port")
parser.add_argument("timeout", type=float, help="Timeout in seconds")

args = parser.parse_args()

open_count = 0
start_time = time.time()

print(f"Scanning {args.ip} ports {args.start_port}-{args.end_port} (timeout {args.timeout}s)...")

with open("scan_report.txt", "w") as f:
    f.write(f"Scan of {args.ip} ports {args.start_port}-{args.end_port} (timeout {args.timeout}s)\n")
    f.write("-" * 50 + "\n")

    for port in range(args.start_port, args.end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(args.timeout)
        result = s.connect_ex((args.ip, port))
        if result == 0:
            print(f"Port {port} is OPEN")
            f.write(f"Port {port} is OPEN\n")
            open_count += 1
        s.close()

    elapsed = time.time() - start_time
    total = args.end_port - args.start_port + 1
    summary = f"Scan complete: {open_count} open, {total - open_count} closed — {elapsed:.2f} seconds"
    print(summary)
    f.write(summary + "\n")
