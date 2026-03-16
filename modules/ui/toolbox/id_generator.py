import time
import secrets
import hashlib


def random_id() -> str:
    """
    Generate a unique, cryptographically secure random hexadecimal identifier.

    The ID is constructed by combining a 48-bit timestamp with a 32-bit random
    value, which is then processed through SHA-256 and truncated to 128 bits
    (16 bytes) for the final hex string representation.

    Returns:
        str: A 32-character hexadecimal string representing the generated ID.
    """
    # Get current timestamp in microseconds and mask to 48 bits (allows for ~8925 years of uniqueness)
    ts: int = int(time.time() * 1_000_000) & ((1 << 48) - 1)

    # Generate 32 bits of cryptographically secure randomness
    rand: int = secrets.randbits(32)

    # Combine timestamp (6 bytes) and random bits (4 bytes) into a single byte sequence
    data: bytes = ts.to_bytes(6, "big") + rand.to_bytes(4, "big")

    # Apply SHA-256 hash to the data and truncate to the first 16 bytes
    digest: bytes = hashlib.sha256(data).digest()[:16]

    # Convert the resulting bytes to a hexadecimal string and return
    return digest.hex()


# Magic
