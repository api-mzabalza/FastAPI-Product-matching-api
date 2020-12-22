from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base

'''
SQLAlchemy models
'''

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    material_code = Column(Integer)
    kff_article = Column(String)
    concurrent = Column(String)
    conc_product_label = Column(String)
    conc_product_price = Column(String)
    conc_product_url = Column(String)
    conc_product_img = Column(String)
    created_at = Column(DateTime)
    conc_product_price = Column(String)
    checked_match = Column(Boolean, default=False)
    is_match = Column(Boolean, default=False)
