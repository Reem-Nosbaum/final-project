from sqlalchemy import Column, Text, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    username = Column(Text(), nullable=False, unique=True)
    password = Column(Text(), nullable=False)
    email = Column(Text(), nullable=False, unique=True)
    user_role = Column(Integer(), ForeignKey('user_roles.id'), unique=False, nullable=False)

    user_roles = relationship('User_Roles', backref=backref('users', uselist=True))

    def __repr__(self):
        return f'< user id={self.id} user name={self.username} password={self.password}'\
               f' email={self.email} user role={self.user_role}>'

    def __str__(self):
        return f'< user id={self.id} user name={self.username} password={self.password}'\
               f' email={self.email} user role={self.user_role}>'