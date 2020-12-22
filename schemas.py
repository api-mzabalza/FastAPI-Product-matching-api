from typing import List, Optional
from pydantic import BaseModel

'''
Pydantic models
'''

class Product(BaseModel):
    id: int
    material_code : int = Field(..., example=293479011)
    kff_article : str
    concurrent : str
    conc_product_label : str
    conc_product_price : float
    conc_product_url : str
    conc_product_img : str
    created_at : datetime
    checked_match : Optional[bool]
    is_match : Optional[bool]


class ProductEntry(BaseModel):
    material_code : int = Field(..., example=293479011)
    kff_article : str = Field(..., example='hammer 150x34x74 cm')
    concurrent : str = Field(..., example='leroymerlin')
    conc_product_label : str = Field(..., example='hammer 1500x34x74 mm')
    conc_product_price : float = Field(..., example=12.12)
    conc_product_url : str = Field(..., example='https://www.leroymerlin.fr/v3/p/produits/cloison-de-separation-atelier-mdf-revetu-noir-effet-metal-l-80-x-h-240-x-p-4cm-e1505562845')
    conc_product_img : str = Field(..., example='https://m2.lmcdn.fr/media/1/5d58251d475ea72a896452d5/.jpg?width=650&height=650&format=jpg&quality=80&fit=bounds')
    created_at : datetime = Field(..., example='2020-12-21T18:12:17.598806')
    checked_match : Optional[bool] = Field(..., example=False)
    is_match : Optional[bool] = Field(..., example=False)

class ProductUpdate(Product):
    pass
