from sqlalchemy import Column, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship, backref

from db_config import Base


class Administrators(Base):
    __tablename__ = 'administrators'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(Text(), nullable=False)
    last_name = Column(Text(), nullable=False)
    user_id = Column(BigInteger(), ForeignKey('users.id'), unique=True)

    user = relationship("Users", backref=backref("administrators", uselist=False, passive_deletes=True))

    def __repr__(self):
        return f'< administrators id = {self.id} first name = {self.first_name}' \
               f' last_name  = {self.last_name} user id = {self.user_id} >'

    def __str__(self):
        return f'< administrators id = {self.id} first name = {self.first_name}' \
               f' last_name  = {self.last_name} user id = {self.user_id} >'

