#!/usr/bin/env python3
"""
Project #7 — Password Strength Checker
Five rungs:
  1. Score a password (length, character classes, common list)
  2. Generate a cryptographic salt
  3. Hash salt+password with SHA-256
  4. Prove the salt matters (same password, two salts, different hashes)
  5. Store (salt, hash) and verify a candidate in constant time

HONEST LIMITS (see README):
  - SHA-256 is FAST. Fast is bad for passwords. Production uses bcrypt/scrypt/argon2.
    We use SHA-256 to teach the salt and the one-way property, not as production crypto.
  - The common-password list is small and illustrative.
  - No entropy model (zxcvbn) — scoring is rule-based, not probabilistic.
"""

import hashlib
import hmac
import secrets
import string

# ---------------------------------------------------------------
# RUNG 1 — Score the password
# ---------------------------------------------------------------

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123",
    "letmein", "monkey", "dragon", "111111", "iloveyou",
    "admin", "welcome", "login", "passw0rd", "starwars",
}

def score_password(pw: str) -> tuple[int, list[str]]:
    """
    Return (score 0-5, list of notes).
    Rules:
      +1 length >= 8
      +1 length >= 12
      +1 has lowercase AND uppercase
      +1 has digit
      +1 has symbol
      -3 if it's in the common list (heavy penalty)
      -1 if it's all one character class (e.g. all digits, all lowercase)
    """
    notes: list[str] = []
    score = 0

    if len(pw) >= 8:
        score += 1
        notes.append("length >= 8")
    else:
        notes.append("TOO SHORT (< 8)")

    if len(pw) >= 12:
        score += 1
        notes.append("length >= 12")

    has_lower = any(c.islower() for c in pw)
    has_upper = any(c.isupper() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_symbol = any(c in string.punctuation for c in pw)

    if has_lower and has_upper:
        score += 1
        notes.append("mixed case")
    if has_digit:
        score += 1
        notes.append("has digit")
    if has_symbol:
        score += 1
        notes.append("has symbol")

    # Penalties
    if pw.lower() in COMMON_PASSWORDS:
        score -= 3
        notes.append("ON COMMON LIST (-3)")

    classes_used = sum([has_lower, has_upper, has_digit, has_symbol])
    if classes_used <= 1:
        score -= 1
        notes.append("single character class (-1)")

    score = max(0, min(5, score))  # clamp 0..5
    return score, notes


def verdict(score: int) -> str:
    return {
        0: "CRITICAL — do not use",
        1: "WEAK",
        2: "WEAK",
        3: "OK",
        4: "STRONG",
        5: "STRONG",
    }[score]


# ---------------------------------------------------------------
# RUNG 2 — Generate a salt
# ---------------------------------------------------------------

def make_salt(n_bytes: int = 16) -> bytes:
    """Cryptographic random salt. 16 bytes = 128 bits."""
    return secrets.token_bytes(n_bytes)


# ---------------------------------------------------------------
# RUNG 3 — Hash salt+password
# ---------------------------------------------------------------

def hash_password(password: str, salt: bytes) -> str:
    """
    sha256( salt || password.encode() ) -> hex digest (64 chars).
    Salt goes FIRST. Order matters, but what matters more is that
    verification repeats the exact same construction.
    """
    combined = salt + password.encode("utf-8")
    return hashlib.sha256(combined).hexdigest()


# ---------------------------------------------------------------
# RUNG 4 — Prove the salt matters
# ---------------------------------------------------------------

def prove_salt_matters(password: str) -> None:
    """
    Same password, two different salts -> two different hashes.
    This is the lesson of #7, made numerical (like #6 made the rhythm numerical).
    """
    salt_a = make_salt()
    salt_b = make_salt()
    hash_a = hash_password(password, salt_a)
    hash_b = hash_password(password, salt_b)

    print("  RUNG 4 — proof the salt matters")
    print(f"    password:   {password!r}")
    print(f"    salt A:     {salt_a.hex()}")
    print(f"    hash A:     {hash_a}")
    print(f"    salt B:     {salt_b.hex()}")
    print(f"    hash B:     {hash_b}")
    print(f"    same hash?  {hash_a == hash_b}   <- must be False")
    print()


# ---------------------------------------------------------------
# RUNG 5 — Store and verify
# ---------------------------------------------------------------

class PasswordStore:
    """
    In-memory store of {username: (salt_hex, hash_hex)}.
    The PLAINTEXT PASSWORD IS NEVER STORED. That is the whole point.
    """
    def __init__(self) -> None:
        self._records: dict[str, tuple[str, str]] = {}

    def register(self, username: str, password: str) -> None:
        salt = make_salt()
        digest = hash_password(password, salt)
        # We store salt and hash. NOT the password.
        self._records[username] = (salt.hex(), digest)

    def verify(self, username: str, candidate: str) -> bool:
        if username not in self._records:
            return False
        salt_hex, stored_hash = self._records[username]
        salt = bytes.fromhex(salt_hex)
        candidate_hash = hash_password(candidate, salt)
        # constant-time compare — timing must not leak
        return hmac.compare_digest(candidate_hash, stored_hash)

    def dump(self) -> None:
        print("  RUNG 5 — stored records (NOTE: no plaintext password anywhere)")
        for user, (salt_hex, digest) in self._records.items():
            print(f"    {user}: salt={salt_hex[:16]}...  hash={digest[:16]}...")
        print()


# ---------------------------------------------------------------
# MAIN — run the full demo
# ---------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("PROJECT #7 — PASSWORD STRENGTH CHECKER")
    print("=" * 60)
    print()

    samples = [
        "password",           # common list, weak
        "Tr0ub4dor&3",        # the classic xkcd example
        "correcthorsebatterystaple",  # long, but single class (letters)
        "P@ssw0rd!",          # looks strong, arguably common-ish
        "9fK!2mQ#7pLx",       # strong
        "12345678",           # common list, single class
    ]

    print("RUNG 1 — scoring")
    print("-" * 60)
    for pw in samples:
        s, notes = score_password(pw)
        print(f"  {pw!r:<30} score={s}  [{verdict(s)}]")
        print(f"    notes: {', '.join(notes)}")
    print()

    prove_salt_matters("Tr0ub4dor&3")

    print("RUNG 5 — register / verify")
    print("-" * 60)
    store = PasswordStore()
    store.register("jctrue", "Tr0ub4dor&3")
    store.register("raven", "9fK!2mQ#7pLx")
    store.dump()

    print("  verify jctrue with correct password:",
          store.verify("jctrue", "Tr0ub4dor&3"))   # True
    print("  verify jctrue with WRONG password:  ",
          store.verify("jctrue", "tr0ub4dor&3"))   # False (case matters)
    print("  verify unknown user:                ",
          store.verify("nobody", "anything"))      # False
    print()
    print("The password never touched the disk. The salt made each hash unique.")
    print("The compare is constant-time. Word Is Born, Son.")


if __name__ == "__main__":
    main()
