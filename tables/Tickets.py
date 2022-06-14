from sqlalchemy import Column, ForeignKey, BigInteger, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    flight_id = Column(BigInteger(), ForeignKey('flights.id'), nullable=False)
    customer_id = Column(BigInteger(), ForeignKey('customers.id'), nullable=False)

    __table_args__ = (UniqueConstraint('flight_id', 'customer_id', name='una_1'),)

    flights = relationship('Flights', backref=backref('tickets', uselist=True))
    customers = relationship('Customers', backref=backref('tickets', uselist=True))

    def __repr__(self):
        return f' ticket id={self.id} flight id={self.flight_id} customer id={self.customer_id}>'

    def __str__(self):
        return f' ticket id={self.id} flight id={self.flight_id} customer id={self.customer_id}>'
