from sqlalchemy import Column, Text, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(Text(), nullable=False)
    last_name = Column(Text(), nullable=False)
    address = Column(Text(), nullable=False)
    phone_number = Column(Text(), unique=True)
    credit_card_number = Column(Text(), unique=True)
    user_id = Column(BigInteger(), ForeignKey('users.id'), unique=True)

    user = relationship("Users", backref=backref("customers", uselist=False, passive_deletes=True))

    def __repr__(self):
        return f'< customers id = {self.id} first name = {self.first_name}' \
               f' last_name  = {self.last_name} address = {self.address} phone number = {self.phone_number}' \
               f'credit card number = {self.credit_card_number} user id = {self.user_id} >'

    def __str__(self):
        return f'< customers id = {self.id} first name = {self.first_name}' \
               f' last_name  = {self.last_name} address = {self.address} phone number = {self.phone_number}' \
               f'credit card number = {self.credit_card_number} user id = {self.user_id} >'
