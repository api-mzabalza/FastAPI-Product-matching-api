from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

host_server = os.environ.get('HOST_SERVER', 'localhost')
db_port = os.environ.get('DB_SERVER_PORT', '5432')
db_name = os.environ.get('DB_NAME', 'kf_pricing')
db_username = os.environ.get('DB_USERNAME', '')
db_password = os.environ.get('DB_PASSWORD', '')

ssl_mode='prefer'

# POSTGRES DATABASE

DATABASE_URL = f'postgresql://{db_username}:{db_password}@{host_server}:{db_port}/{db_name}?sslmode={ssl_mode}'


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()