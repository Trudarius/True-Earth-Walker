counts = {}

with open("sample.log", "r") as f:
    for line in f:
        parts = line.split()
        if len(parts) == 0:
            continue
        ip = parts[0]

        if ip in counts:
            counts[ip] += 1
        else:
            counts[ip] = 1

print(counts)

