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

	airline_company = relationship('Airline_Companies', backref=backref('flights', uselist=True, passive_deletes=True))
	origin_county = relationship('Countries', foreign_keys=[origin_country_id], backref=backref("oc_flights", uselist=True))
	destination_county = relationship('Countries', foreign_keys=[destination_country_id], backref=backref("dc_flights", uselist=True))

	def __repr__(self):
		return f'< flight id={self.id} airline airline_company id={self.airline_company_id}' \
			   f' origin_county country id={self.origin_country_id}' \
			   f' destination_county country id={self.destination_country_id} departure time={self.departure_time}' \
			   f' landing time={self.landing_time} remaining tickets={self.remaining_tickets}>'

	def __str__(self):
		return f'< flight id={self.id} airline airline_company id={self.airline_company_id}' \
			   f' origin_county country id={self.origin_country_id}' \
			   f' destination_county country id={self.destination_country_id} departure time={self.departure_time}' \
			   f' landing time={self.landing_time} remaining tickets={self.remaining_tickets}>'

	def data_for_web(self):
		return {'id': self.id, 'airline_company': self.airline_company.name, 'origin_county': self.origin_county.name,
				'destination_county': self.destination_county.name, 'departure_time': str(self.departure_time),
				'landing_time': str(self.landing_time),
				'remaining_tickets': self.remaining_tickets}
