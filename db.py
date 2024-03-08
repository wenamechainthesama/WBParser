from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    String,
    Integer,
)

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    name = Column(String)
    price = Column(Integer)
    discounted_price = Column(Integer)
    path = Column(String)
    images = Column(String)
    description = Column(String)
    characteristics = Column(String)
    article = Column(Integer, primary_key=True)

    def __init__(
        self,
        name,
        price,
        discounted_price,
        path,
        images,
        description,
        characteristics,
        article,
    ):
        self.name = name
        self.price = price
        self.discounted_price = discounted_price
        self.path = path
        self.images = images
        self.description = description
        self.characteristics = characteristics
        self.article = article


engine = create_engine("sqlite:///products.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
