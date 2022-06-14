from sqlalchemy import Column, Integer, Text
from db_config import Base


class Countries(Base):
    __tablename__ = 'countries'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(Text(), nullable=False, unique=True)

    def __repr__(self):
        return f'<Countries id = {self.id} name = {self.name} >'

    def __str__(self):
        return f'<Countries id = {self.id} name = {self.name}>'
