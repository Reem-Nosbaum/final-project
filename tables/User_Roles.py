from sqlalchemy import Column, BigInteger, Text
from db_config import Base


class User_Roles(Base):
    __tablename__ = 'user_roles'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    role_name = Column(Text(), unique=True)

    def __repr__(self):
        return f'< role id={self.id} role name={self.role_name}>'

    def __str__(self):
        return f'<role id={self.id} role name={self.role_name}>'
