from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    temperature = Column(Integer)
    wind_str = Column(Integer)
    wind_dir = Column(Integer)
