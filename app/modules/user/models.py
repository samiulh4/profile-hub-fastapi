import enum
from sqlalchemy import Column, DateTime, Enum, Integer, String, Date, Boolean, false
from app.core.database import Base

class GenderEnum(enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class UserType(Base):
    __tablename__ = "users_type"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(10), nullable=False, unique=True, index=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

class UserGender(Base):
    __tablename__ = "users_gender"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id = Column(Integer, primary_key=True, index=True)
    gender_name = Column(String(10), nullable=False, unique=True, index=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id = Column(Integer, primary_key=True, index=True)
    user_identity = Column(String(255), unique=True, index=True, nullable=False)
    user_email = Column(String(255), nullable=False)
    user_mobile = Column(String(30), nullable=False)
    user_type = Column(String(10), server_default="USER", nullable=False) # join with users_type table by type_name
    user_password = Column(String(255), nullable=False)
    user_full_name = Column(String(255), nullable=False)
    user_gender = Column(Enum(GenderEnum), nullable=False) # join with users_gender table by gender_name
    user_birthday = Column(Date, nullable=False)
    user_birth_certificate = Column(String(50), nullable=True)
    user_national_identity = Column(String(50), nullable=True)
    user_passport = Column(String(50), nullable=True)
    user_photo_id = Column(Integer, nullable=True)
    user_signature_id = Column(Integer, nullable=True)
    user_status = Column(Boolean, nullable=False, default=0, server_default=false())
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
