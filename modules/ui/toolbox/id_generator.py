import time
import secrets
import hashlib

def random_id():

    ts = int(time.time() * 1_000_000) & ((1 << 48) - 1)
    rand = secrets.randbits(32)
    data = ts.to_bytes(6, "big") + rand.to_bytes(4, "big")
    digest = hashlib.sha256(data).digest()[:16]

    return digest.hex()

#Magic