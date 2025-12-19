from datetime import datetime, timezone
import base64
import pyotp
from pathlib import Path

SEED_PATH = Path("/data/seed.txt")

def main():
    if not SEED_PATH.exists():
        print("Seed not found")
        return

    hex_seed = SEED_PATH.read_text().strip()

    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)
    code = totp.now()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
