from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///secure_pass.db"  # or your actual database URL

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

class AuthorizedVehicle(Base):
    __tablename__ = "authorized_vehicles"
    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, nullable=False)
    owner_name = Column(String, nullable=True)
    vehicle_type = Column(String, nullable=True)

class AccessLog(Base):
    __tablename__ = "access_logs"
    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    confidence = Column(Integer, nullable=False)
    verified = Column(Boolean, default=False)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)
