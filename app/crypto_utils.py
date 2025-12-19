import base64
import pyotp
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    ciphertext = base64.b64decode(encrypted_seed_b64)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    seed = plaintext.decode("utf-8").strip()

    if len(seed) != 64:
        raise ValueError("Invalid seed length")

    int(seed, 16)  # validate hex
    return seed


def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode("utf-8")


def generate_totp(hex_seed: str) -> str:
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.now()


def verify_totp(hex_seed: str, code: str) -> bool:
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=1)
