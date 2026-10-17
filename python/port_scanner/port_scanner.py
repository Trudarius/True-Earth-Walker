ports = [22, 21, 53, 80, 443, 445]

for port in ports:
    s = socket.socket(...)
    s.settimeout(1)
ports = [22, 21, 53, 80, 443, 445]

for port in ports:
    s = socket.socket(...)
    s.settimeout(1)
    result = s.connect_ex((ip, port))
    if result == 0:
       print(f"Port {port} is OPEN")
    else:
       print(f"Port {port} is CLOSED - code: {result}")
    s.close()
