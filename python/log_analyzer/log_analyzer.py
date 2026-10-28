# ============================================================
# LOG ANALYZER v2 — Project #6
# check_that_ninja — every ninja, every time.
# ============================================================
# RUNG 5: Same detection as rung 4, but with a
# findings-first report. Analysts get the answer
# in the first five lines, then evidence below.
# ============================================================

from datetime import datetime

LOG_FILE = "sample.log"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

MIN_HITS = 4
MAX_DEVIATION = 5.0

# ---- Gather timestamps per destination ----
destination_times = {}

with open(LOG_FILE, "r") as f:
    for line in f:
        parts = line.split()
        if len(parts) != 5:
            continue

        stamp = f"{parts[0]} {parts[1]}"
        destination = parts[4]
        when = datetime.strptime(stamp, TIME_FORMAT)

        destination_times.setdefault(destination, []).append(when)

# ---- Measure and classify ----
beacons = []
normals = []
too_few = []

for destination, times in sorted(destination_times.items()):
    times.sort()
    hits = len(times)

    if hits < MIN_HITS:
        too_few.append((destination, hits))
        continue

    intervals = [(times[i] - times[i - 1]).total_seconds()
                 for i in range(1, hits)]
    mean_interval = sum(intervals) / len(intervals)
    max_deviation = max(abs(x - mean_interval) for x in intervals)

    if max_deviation <= MAX_DEVIATION:
        beacons.append((destination, hits, mean_interval, max_deviation, intervals))
    else:
        normals.append((destination, hits, mean_interval, max_deviation, intervals))

# ---- SUMMARY FIRST ----
print("=" * 60)
print("LOG ANALYZER v2 — BEACON DETECTION REPORT")
print("=" * 60)
print(f"Log file: {LOG_FILE}")
print(f"Threshold: ±{MAX_DEVIATION}s deviation from mean, min {MIN_HITS} hits")
print()
print(f"🚨 SUSPECTED BEACONS: {len(beacons)}")
print(f"✅ CLEARED (normal rhythm): {len(normals)}")
print(f"⏸️  TOO FEW HITS: {len(too_few)}")
print("=" * 60)

# ---- Details: beacons first ----
if beacons:
    print("\n--- SUSPECTED BEACONS ---")
    for dest, hits, mean, dev, ivs in beacons:
        print(f"\n🚨 {dest}")
        print(f"   {hits} hits | mean interval {mean:.1f}s | max deviation {dev:.1f}s")
        print(f"   intervals: {ivs}")

if normals:
    print("\n--- NORMAL (cleared) ---")
    for dest, hits, mean, dev, ivs in normals:
        print(f"\n   {dest}")
        print(f"   {hits} hits | mean interval {mean:.1f}s | max deviation {dev:.1f}s")

if too_few:
    print("\n--- TOO FEW HITS TO JUDGE ---")
    for dest, hits in too_few:
        print(f"   {dest}  ({hits} hits)")

print("\n" + "=" * 60)
print("check_that_ninja — every ninja, every time.")
print("=" * 60)
