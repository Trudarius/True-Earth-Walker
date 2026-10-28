# Project #7 — Password Strength Checker

Five rungs: score, salt, hash, verify, prove.

## What it does
- Scores a password by length, character classes, and a common-password list.
- Generates a cryptographic salt (secrets.token_bytes, 16 bytes).
- Hashes salt+password with SHA-256.
- Proves the same password hashes differently with different salts.
- Stores (salt, hash) and verifies in constant time (hmac.compare_digest).

## The lesson
The plaintext password is never stored. The salt guarantees uniqueness.
Constant-time compare prevents timing leaks.

## Honest limits
- SHA-256 is FAST. Fast is BAD for passwords. Production uses bcrypt,
  scrypt, or argon2 with a cost factor. We use SHA-256 here to teach the
  salt and the one-way property, not as production crypto.
- The common-password list is small and illustrative.
- No entropy model (zxcvbn). Scoring is rule-based.
