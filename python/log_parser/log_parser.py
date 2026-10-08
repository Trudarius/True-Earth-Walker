counts = {}
attacks = {}

with open("sample.log", "r") as f:
    for line in f:
        parts = line.split()
        if len(parts) == 0:
            continue

        ip = parts[0]

        # Shape guard
        if len(parts) >= 8:
            status = parts[7]         # long shape
            path = parts[5]
        elif len(parts) >= 7:
            status = parts[6]         # short shape
            path = parts[5]
        else:
            continue

        # Count every hit
        counts[ip] = counts.get(ip, 0) + 1

        # Flag 4xx as attacks
        if int(status) >= 400:
            attacks.setdefault(ip, []).append((int(status), path))

# Report
print("=== FLAGGED (threshold >= 6) ===")
for ip, count in counts.items():
    if count >= 6:
        print(f"FLAG: {ip} - {count} requests")

print("\n=== ATTACK SIGNALS (4xx) ===")
for ip, hits in attacks.items():
    print(f"\n{ip}:")
    for status, path in hits:
        print(f"  {status}  {path}")
