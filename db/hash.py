from passlib.context import CryptContext

# Encrypt passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
class Hash:
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify(hashed_password, plain_password):
        return pwd_context.verify(plain_password, hashed_password)