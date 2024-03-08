from sqlalchemy import (
    create_engine,
    ForeignKey,
    Column,
    String,
    Integer,
    CHAR,
    PickleType,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    name = Column("name", String)
    price = Column("price", Integer)
    discounted_price = Column("discounted_price", Integer)
    path = Column("Путь", String)
    images = Column("Фото", PickleType)
    description = Column("Описание", String)
    characteristics = Column(PickleType)

    def __init__(
        self, name, price, discounted_price, path, images, description, characteristics
    ):
        self.name = name
        self.price = price
        self.discounted_price = discounted_price
        self.path = path
        self.images = images
        self.description = description
        self.characteristics = characteristics


# engine = create_engine("sqlite:///products.db", echo=True)
# Base.metadata.create_all(bind=engine)

# Session = sessionmaker(bind=engine)
# session = Session()
