import settings
import os
from fastapi import FastAPI
import databases, sqlalchemy
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta
from typing import List, Optional
from database import SessionLocal, engine

host_server = os.environ.get('HOST_SERVER', 'localhost')
db_port = os.environ.get('DB_SERVER_PORT', '5432')
db_name = os.environ.get('DB_NAME', 'kf_pricing')
db_username = os.environ.get('DB_USERNAME', '')
db_password = os.environ.get('DB_PASSWORD', '')

ssl_mode='prefer'

# POSTGRES DATABASE

DATABASE_URL = f'postgresql://{db_username}:{db_password}@{host_server}:{db_port}/{db_name}?sslmode={ssl_mode}'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

matching_products = sqlalchemy.Table(
    "matching_products",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer),
    sqlalchemy.Column('material_code', sqlalchemy.Integer),
    sqlalchemy.Column('kff_article', sqlalchemy.String),
    sqlalchemy.Column('concurrent', sqlalchemy.String),
    sqlalchemy.Column('conc_product_label', sqlalchemy.String),
    sqlalchemy.Column('conc_product_price', sqlalchemy.Float),
    sqlalchemy.Column('conc_product_url', sqlalchemy.String),
    sqlalchemy.Column('conc_product_img', sqlalchemy.String),
    sqlalchemy.Column('created_at', sqlalchemy.TIMESTAMP),
    sqlalchemy.Column('checked_match', sqlalchemy.Boolean),
    sqlalchemy.Column('is_match', sqlalchemy.Boolean)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
#     DATABASE_URL, connect_args={'check_same_thread': False}
#     # DATABASE_URL, pool_size=3, max_overflow=0
 )

metadata.create_all(engine)

# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Models

class Product(BaseModel):
    id: Optional[int]
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

# Properties to receive on item update
class ProductUpdate(Product):
    pass

#     def update(self, **kwargs):
#         for key, value in kwargs.items():
#             if hasattr(self, key):
#                 setattr(self, key, value)

# class ProductUpdate(BaseModel):
#     id : int = Field(..., example="Enter your Id")
#     material_code : int = Field(..., example=293479011)
#     kff_article : str = Field(..., example='hammer 150x34x74 cm')
#     concurrent : str = Field(..., example='leroymerlin')
#     conc_product_label : str = Field(..., example='hammer 1500x34x74 mm')
#     conc_product_price : float = Field(..., example=12.12)
#     conc_product_url : str = Field(..., example='https://www.leroymerlin.fr/v3/p/produits/cloison-de-separation-atelier-mdf-revetu-noir-effet-metal-l-80-x-h-240-x-p-4cm-e1505562845')
#     conc_product_img : str = Field(..., example='https://m2.lmcdn.fr/media/1/5d58251d475ea72a896452d5/.jpg?width=650&height=650&format=jpg&quality=80&fit=bounds')
#     created_at : datetime = Field(..., example='2020-12-21T18:12:17.598806')
#     checked_match : bool = Field(..., example=False)
#     is_match : Optional[bool] = Field(..., example=False)



app = FastAPI()

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/products", response_model=List[Product])
async def find_all_products():
    query = matching_products.select()
    return await database.fetch_all(query)

@app.get("/products/to_check")
async def find_all_products(checked_match: bool):
    query = matching_products.select().where(matching_products.c.checked_match == checked_match)
    data =  await database.fetch_one(query)
    material_code = data['material_code']
    query = matching_products.select().where(matching_products.c.material_code == material_code)
    return await database.fetch_one(query)

@app.post("/products", response_model=Product)
async def register_product(product: ProductEntry):
    # gID = str(uuid.uuid1())
    query = matching_products.insert().values(
        material_code = product.material_code,
        kff_article = product.kff_article,
        concurrent = product.concurrent,
        conc_product_label = product.conc_product_label,
        conc_product_price = product.conc_product_price,
        conc_product_url = product.conc_product_url,
        conc_product_img = product.conc_product_img,
    )
    await database.execute(query)

    return {**product.dict()}

@app.get('/products/{productId}', response_model=Product)
async def find_product_by_id(productId: int):
    query = matching_products.select().where(matching_products.c.id == productId)
    return await database.fetch_one(query)


@app.put('/products/check/{productId}', response_model=Product)
async def check_product(productId: int):
    query = matching_products.update(). \
        where(matching_products.c.id == productId). \
        values(checked_match = 1)

    await database.execute(query)
    return await find_product_by_id(product.id)


@app.put('/products/match/{productId}', response_model=Product)
async def match_product(productId: int):
    query = matching_products.update(). \
        where(matching_products.c.id == productId). \
        values(is_match = 1)
    await database.execute(query)

    product = await find_product_by_id(productId)

    query = matching_products.update(). \
        where(matching_products.c.material_code == product['material_code']). \
        values(checked_match = 1)

    return product


@app.put("/products")
async def update_product(product: ProductUpdate):
    test = {
        key: value for key, value in product if value
    }
    print(test)
    # return test
    # matching_products.filter(matching_products.c.id == product.id).update(test)
    query = matching_products.update(). \
        where(matching_products.c.id == product.id). \
        values(
            material_code = product.material_code,
            kff_article = product.kff_article,
            concurrent = product.concurrent,
            conc_product_label = product.conc_product_label,
            conc_product_price = product.conc_product_price,
            conc_product_url = product.conc_product_url,
            conc_product_img = product.conc_product_img,
            checked_match = product.checked_match,
            is_match = product.is_match
        )

    await database.execute(query)

    return await find_product_by_id(product.id)


