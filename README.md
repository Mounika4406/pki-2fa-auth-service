PKI-Based 2FA Authentication Microservice (Dockerized)

This project implements a secure Two-Factor Authentication (2FA) microservice using FastAPI, Public Key Infrastructure (PKI), Time-based One-Time Passwords (TOTP), Docker, and cron automation.
It demonstrates secure cryptographic practices, containerized deployment, and automated background processing.

✨ Features

Secure TOTP-based 2FA generation and verification

Encrypted seed handling using PKI

Git commit integrity verification using RSA signatures

Fully Dockerized microservice

Cron job that logs 2FA codes periodically

Persistent seed storage inside container

Clean API design using FastAPI

🧰 Technology Stack
Category	Technology
Language	Python 3.11
Framework	FastAPI
Cryptography	RSA (SHA-256, PSS, OAEP)
OTP	TOTP (RFC-compliant)
Containerization	Docker, Docker Compose
Scheduler	Linux Cron
📂 Project Structure
pki-2fa-auth-service/
├── app/
│   ├── main.py
│   ├── crypto_utils.py
│   └── __init__.py
├── scripts/
│   └── log_2fa_cron.py
├── cron/
│   └── 2fa-cron
├── data/                  # created at runtime inside container
├── student_private.pem
├── student_public.pem
├── instructor_public.pem
├── sign_commit.py
├── encrypt_signature.py
├── encrypted_seed.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

🚀 Setup & Execution
Step 1: Build and Start the Service
docker compose build --no-cache
docker compose up -d


Verify container is running:

docker ps


Expected container name:

pki-2fa-auth-service-app-1

🔑 PKI Commit Verification
Step 2: Sign Latest Commit
git log -1 --format=%H
python sign_commit.py


Paste the commit hash when prompted

Copy the printed Base64 signature

Step 3: Encrypt the Signature
python encrypt_signature.py


Paste the Base64 signature

Copy FINAL ENCRYPTED SIGNATURE

Submit this value in the evaluation form

🌱 Seed Decryption

Decrypt the encrypted seed received from the instructor:

curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_seed\":\"$(cat encrypted_seed.txt)\"}"


Verify seed storage inside container:

docker exec pki-2fa-auth-service-app-1 sh -c "cat /data/seed.txt"

🔢 2FA API Endpoints
Generate 2FA Code
curl http://localhost:8080/generate-2fa


Example response:

{
  "code": "267113",
  "valid_for": 30
}

Verify 2FA Code
curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d '{"code":"267113"}'


Response:

{"valid": true}


Invalid code example:

{"valid": false}

⏱ Cron Job Verification

Check cron configuration:

docker exec pki-2fa-auth-service-app-1 crontab -l


View logged 2FA codes:

docker exec pki-2fa-auth-service-app-1 sh -c "tail -5 /cron/last_code.txt"


Example output:

2025-12-19 03:59:01 - 2FA Code: 875338

🔐 Security Considerations

TOTP seed is never exposed through APIs

Commit authenticity enforced using PKI

SHA-256 used for hashing and signatures

Time-bound TOTP codes automatically expire

Application isolated inside Docker container

✅ Final Status

All APIs functioning correctly

PKI verification completed successfully

Cron automation verified

Docker build reproducible

Secure seed storage confirmed

🎓 Conclusion

This project demonstrates a practical implementation of a PKI-verified 2FA microservice using modern cryptographic standards and containerization techniques. It is suitable for academic evaluation and reflects real-world secure system design practices.
