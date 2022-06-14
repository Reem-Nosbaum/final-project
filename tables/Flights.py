from sqlalchemy import Column, Integer, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Flights(Base):
    __tablename__ = 'flights'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger(), ForeignKey('airline_companies.id'), nullable=False)
    origin_country_id = Column(Integer(), ForeignKey('countries.id'), unique=False, nullable=False)
    destination_country_id = Column(Integer(), ForeignKey('countries.id'), unique=False, nullable=False)
    departure_time = Column(DateTime(), unique=False, nullable=False)
    landing_time = Column(DateTime(), unique=False, nullable=False)
    remaining_tickets = Column(Integer())

    company = relationship('Airline_Companies', backref=backref('flights', uselist=True))
    origin = relationship("Countries", foreign_keys=[origin_country_id], uselist=True)
    destination = relationship("Countries", foreign_keys=[destination_country_id], uselist=True)

    def __repr__(self):
        return f'< flight id={self.id} airline company id={self.airline_company_id}' \
               f' origin country id={self.origin_country_id}'\
               f' destination country id={self.destination_country_id} departure time={self.departure_time}' \
               f' landing time={self.landing_time} remaining tickets={self.remaining_tickets}>'

    def __str__(self):
        return f'< flight id={self.id} airline company id={self.airline_company_id}' \
               f' origin country id={self.origin_country_id}'\
               f' destination country id={self.destination_country_id} departure time={self.departure_time}' \
               f' landing time={self.landing_time} remaining tickets={self.remaining_tickets}>'
