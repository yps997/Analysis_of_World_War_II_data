from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Country(Base):
    __tablename__ = 'countries'
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String(100), unique=True, nullable=False)
    cities = relationship('City', backref='country', lazy=False)

class City(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(100))
    country_id = Column(Integer, ForeignKey('countries.country_id'), nullable=False)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    targets = relationship('Target', backref='city', lazy=False)

class TargetType(Base):
    __tablename__ = 'targettypes'
    target_type_id = Column(Integer, primary_key=True)
    target_type_name = Column(String(255), unique=True, nullable=False)
    targets = relationship('Target', backref='target_type', lazy=False)

class Target(Base):
    __tablename__ = 'targets'
    target_id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey('missions.mission_id'))
    target_industry = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.city_id'), nullable=False)
    target_type_id = Column(Integer, ForeignKey('targettypes.target_type_id'))
    target_priority = Column(Integer)

class Mission(Base):
    __tablename__ = 'missions'
    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Numeric(10,2))
    attacking_aircraft = Column(Numeric(10,2))
    bombing_aircraft = Column(Numeric(10,2))
    aircraft_returned = Column(Numeric(10,2))
    aircraft_failed = Column(Numeric(10,2))
    aircraft_damaged = Column(Numeric(10,2))
    aircraft_lost = Column(Numeric(10,2))
    targets = relationship('Target', backref='mission', lazy=False)