from passlib.context import CryptContext


class Hash:
    pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")

    @classmethod
    def hash_password(self, password: str) -> str:
        hashed_password = self.pwd_context.hash(password)
        return hashed_password

    @classmethod
    def verify_hashed_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
