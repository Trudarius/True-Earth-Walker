# Log Analyzer v2 — Project #6

C2 beacon detection from connection logs.

## What it does
Reads `sample.log`, groups connections by destination,
calculates the interval between each destination's hits,
and flags destinations whose intervals are suspiciously
regular — the signature of a C2 beacon.

## Detection rule
- Requires >=4 hits (so >=3 intervals) to judge.
- Flags if all intervals are within +/-5s of their mean.

Both numbers are **choices, not facts** — a real detection
engineer tunes them against false positives and false negatives.
The beacons in this sample jitter +/-2s; Google scatters +/-100s.
+/-5s separates them cleanly.

## Run
    python3 log_analyzer.py

Save the output for the record:
    python3 log_analyzer.py 2>&1 | tee report_output.txt

## Sample finding (2026-10-27)
- SUSPECTED: 203.0.113.42:443 — 6 hits, ~59.8s interval, from 192.168.1.50
- SUSPECTED: 198.51.100.23:8443 — 6 hits, ~60.0s interval, from 10.0.0.77
- CLEARED:   172.217.14.206:443 — normal (Google, daytime, irregular)

## Known limits
- Jittery beacons (>+/-5s deviation) will slip through.
- Beacons that rotate across many destinations won't
  accumulate enough hits on any single one.
- Only looks at one log file, one source at a time.

## Next
- Jitter detection (variance instead of max deviation).
- Multi-log correlation.
- Allowlist for known-good destinations.

# check_that_ninja — every ninja, every time.
