"""AES-256-GCM file encryption using a password.

Requires: pip install cryptography

File format: salt (16 bytes) | nonce (12 bytes) | ciphertext + auth tag
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

SALT_SIZE = 16
NONCE_SIZE = 12


def _derive_key(password: str, salt: bytes) -> bytes:
    """Turn a password into a 256-bit key using scrypt."""
    kdf = Scrypt(salt=salt, length=32, n=2**15, r=8, p=1)
    return kdf.derive(password.encode("utf-8"))


def encrypt_file(in_path: str, out_path: str, password: str) -> None:
    """Encrypt in_path with AES-256-GCM and write the result to out_path."""
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)  # must be unique per encryption
    key = _derive_key(password, salt)

    with open(in_path, "rb") as f:
        plaintext = f.read()

    ciphertext = AESGCM(key).encrypt(nonce, plaintext, None)

    with open(out_path, "wb") as f:
        f.write(salt + nonce + ciphertext)


def decrypt_file(in_path: str, out_path: str, password: str) -> None:
    """Decrypt a file made by encrypt_file. Raises InvalidTag if the
    password is wrong or the file was tampered with."""
    with open(in_path, "rb") as f:
        data = f.read()

    salt = data[:SALT_SIZE]
    nonce = data[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = data[SALT_SIZE + NONCE_SIZE:]

    key = _derive_key(password, salt)
    plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)

    with open(out_path, "wb") as f:
        f.write(plaintext)


if __name__ == "__main__":
    encrypt_file("secret.txt", "secret.txt.enc", "correct horse battery staple")
    decrypt_file("secret.txt.enc", "secret_decrypted.txt", "correct horse battery staple")
