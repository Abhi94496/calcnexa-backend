from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# def hash_password(password: str):
#     return pwd_context.hash(password)

def hash_password(password: str) -> str:
    # pre-hash password to remove 72 byte limit
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha256_hash)

def verify_password(password: str, hashed_password: str) -> bool:
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)