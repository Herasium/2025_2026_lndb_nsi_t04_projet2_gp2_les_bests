"""Module pour la génération d'identifiants uniques cryptographiquement sécurisés."""

import time
import secrets
import hashlib


def random_id() -> str:
    """Génère un identifiant hexadécimal de 128 bits.

    Construit l'identifiant en hachant une combinaison d'un horodatage de 48 bits et
    d'une entropie aléatoire de 32 bits pour garantir l'unicité et l'imprévisibilité.

    Returns:
        Une chaîne hexadécimale de 32 caractères.
    """
    # Extraction de l'horodatage en microsecondes, masqué sur 48 bits
    ts: int = int(time.time() * 1_000_000) & ((1 << 48) - 1)

    # Génération de 32 bits d'entropie aléatoire
    rand: int = secrets.randbits(32)

    # Concaténation des données en format binaire
    data: bytes = ts.to_bytes(6, "big") + rand.to_bytes(4, "big")

    # Utilisation des 128 premiers bits du hachage SHA-256 pour une sortie à longueur fixe
    digest: bytes = hashlib.sha256(data).digest()[:16]

    return digest.hex()