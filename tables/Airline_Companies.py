from sqlalchemy import Column, BigInteger, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Airline_Companies(Base):
	__tablename__ = 'airline_companies'

	id = Column(BigInteger(), primary_key=True, autoincrement=True)
	name = Column(Text(), nullable=False, unique=True)
	countries_id = Column(BigInteger(), ForeignKey('countries.id'), unique=False, nullable=False, )
	user_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), unique=True)

	country = relationship('Countries')
	user = relationship("Users", backref=backref("airline_companies", uselist=False, passive_deletes=True))

	def __repr__(self):
		return f'< Airline_Companies id = {self.id} name = {self.name}' \
			   f' country id = {self.countries_id} user id = {self.user_id} >'

	def __str__(self):
		return f'< Airline_Companies id = {self.id} name = {self.name}' \
			   f' country id = {self.countries_id} user id = {self.user_id} >'

	def get_dictionary(self):
		return {'id': self.id,
				'name': self.name,
				'country': self.country.name,
				'user_id': self.user_id}
