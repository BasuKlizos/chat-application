from passlib.context import CryptContext


class Hash:
    """Hashing utility class."""
    pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")

    @classmethod
    def hash_password(self, password: str) -> str:
        """Hashes the given password."""
        hashed_password = self.pwd_context.hash(password)
        return hashed_password

    @classmethod
    def verify_hashed_password(self, password: str, hashed_password: str) -> bool:
        """Verifies the given password against the hashed password."""
        return self.pwd_context.verify(password, hashed_password)
