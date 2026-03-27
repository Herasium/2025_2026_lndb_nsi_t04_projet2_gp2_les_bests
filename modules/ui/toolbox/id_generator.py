"""Module for generating cryptographically secure unique identifiers."""

import time
import secrets
import hashlib


def random_id() -> str:
    """Generates a 128-bit hexadecimal identifier.

    Constructs the ID by hashing a combination of a 48-bit timestamp and
    32-bit random entropy to ensure uniqueness and unpredictability.

    Returns:
        A 32-character hexadecimal string.
    """
    ts: int = int(time.time() * 1_000_000) & ((1 << 48) - 1)

    rand: int = secrets.randbits(32)

    data: bytes = ts.to_bytes(6, "big") + rand.to_bytes(4, "big")

    # Use the first 128 bits of the SHA-256 hash for fixed-length output
    digest: bytes = hashlib.sha256(data).digest()[:16]

    return digest.hex()
