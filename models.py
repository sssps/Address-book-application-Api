from sqlalchemy import Boolean, Column, Integer, String, Float
from db_handler import Base


class Address(Base):
    """
    This is a model class. which is having the movie table structure with all the constraint
    """
    __tablename__ = "Address"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    address_name = Column(String(255), index=True, nullable=False)
    latitude = Column(Float, index=True, nullable=False)
    longitude = Column(Float, index=True, nullable=False)