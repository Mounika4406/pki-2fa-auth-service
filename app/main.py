from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import time

from cryptography.hazmat.primitives import serialization
from app.crypto_utils import decrypt_seed, generate_totp, verify_totp

app = FastAPI()

SEED_PATH = Path("/data/seed.txt")
PRIVATE_KEY_PATH = Path("student_private.pem")


class DecryptRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


def load_private_key():
    try:
        with open(PRIVATE_KEY_PATH, "rb") as f:
            return serialization.load_pem_private_key(
                f.read(),
                password=None
            )
    except Exception:
        raise HTTPException(status_code=500, detail="Private key load failed")


@app.post("/decrypt-seed")
def decrypt_seed_api(req: DecryptRequest):
    try:
        private_key = load_private_key()
        seed = decrypt_seed(req.encrypted_seed, private_key)

        SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
        SEED_PATH.write_text(seed)

        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")


@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    seed = SEED_PATH.read_text().strip()
    code = generate_totp(seed)

    valid_for = 30 - (int(time.time()) % 30)
    return {"code": code, "valid_for": valid_for}


@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not SEED_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    seed = SEED_PATH.read_text().strip()
    valid = verify_totp(seed, req.code)

    return {"valid": valid}
