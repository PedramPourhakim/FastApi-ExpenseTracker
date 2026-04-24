from sqlalchemy import Column, UUID, String, ForeignKey
from core.database import Base
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(250), nullable=False)
    password = Column(String, nullable=False)
    person_id = Column(String, ForeignKey("people.id"))

    def __repr__(self):
        return (
            f"User(id={self.id}, username={self.username},person_id={self.person_id})"
        )

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, plain_text):
        self.password = self.hash_password(plain_text)
