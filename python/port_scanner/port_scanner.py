# NOTE (2026-10-27): Threading added Oct 25.
# Benchmark on 127.0.0.1 ports 1-8001 (0.5s timeout):
#   sequential: 2.61s
#   threaded (20 workers): 11.75s
# Threading is SLOWER on loopback because the bottleneck is thread
# overhead and GIL contention, not network wait. On a real remote
# target, threading is expected to win. Re-benchmark against a
# remote host before concluding threading "failed."

import socket
import argparse
import time
import threading

parser = argparse.ArgumentParser(description="True's Port Scanner")
parser.add_argument("ip", help="Target IP address")
parser.add_argument("start_port", type=int, help="Start port")
parser.add_argument("end_port", type=int, help="End port")
parser.add_argument("timeout", type=float, help="Timeout in seconds")
parser.add_argument("workers", type=int, help="Number of threads")

args = parser.parse_args()

open_count = 0
lock = threading.Lock()
start_time = time.time()

print(f"Scanning {args.ip} ports {args.start_port}-{args.end_port} (timeout {args.timeout}s, {args.workers} workers)...")


def scan_port(port):
    global open_count
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(args.timeout)
    result = s.connect_ex((args.ip, port))
    if result == 0:
        with lock:
            print(f"Port {port} is OPEN")
            f.write(f"Port {port} is OPEN\n")
            open_count += 1
        try:
            s.settimeout(2)
            banner = s.recv(1024).decode(errors="ignore").strip()
            if banner:
                with lock:
                    print(f"  Banner: {banner}")
                    f.write(f"  Banner: {banner}\n")
        except:
            pass
    s.close()


with open("scan_report.txt", "w") as f:
    f.write(f"Scan of {args.ip} ports {args.start_port}-{args.end_port} (timeout {args.timeout}s, {args.workers} workers)\n")
    f.write("-" * 50 + "\n")

    threads = []
    for port in range(args.start_port, args.end_port + 1):
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()

        if len(threads) >= args.workers:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    elapsed = time.time() - start_time
    total = args.end_port - args.start_port + 1
    summary = f"Scan complete: {open_count} open, {total - open_count} closed — {elapsed:.2f} seconds"
    print(summary)
    f.write(summary + "\n")
