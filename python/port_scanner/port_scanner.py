import socket

target_ip = "127.0.0.1"
ports = [22, 21, 53, 80, 443, 445]

for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target_ip, port))
    if result == 0:
        print(f"Port {port} is OPEN")
    else:
        print(f"Port {port} is CLOSED — code: {result}")
    s.close()
