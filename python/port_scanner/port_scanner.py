import socket

target_ip = "127.0.0.1"
target_port = 22

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)

result = s.connect_ex((target_ip, target_port))

if result == 0:
    print(f"Port {target_port} is OPEN")
else:
    print(f"Port {target_port} is CLOSED — code: {result}")

s.close()
