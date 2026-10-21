import argon2

ph = argon2.PasswordHasher()  # initiate hasher
def hash_password(password: str) -> str:
    """Return a secure hash of password suitable for database storage."""
    return ph.hash(password)  # hasher generates hash for password, includes salt

def verify_password(password_hash: str, password: str) -> bool:
    """Return True if password matches stored_hash, False otherwise."""
    try:
        return ph.verify(password_hash, password)
    except Exception:
        return False

# the argon2 documentation was referenced but it's hard not to make it really similar to the example


if __name__ == '__main__':
    hashed_password = hash_password('morton')
    print(verify_password(hashed_password, "morton"))
    print(verify_password(hashed_password, "morton."))