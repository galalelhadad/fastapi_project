from sqlalchemy import create_engine,URL
from sqlalchemy.orm import sessionmaker , declarative_base
from .config import settings

import psycopg2


SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=int(settings.database_port),
    database=settings.database_name,
    query={
        "sslmode": settings.database_sslmode,
    },
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

# SQLALCHEMY_DATABASE_URL="postgresql://<user>:<password>@<host>/<database_bame>"
# SQLALCHEMY_DATABASE_URL=f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


# engine=create_engine(SQLALCHEMY_DATABASE_URL)
Sessionlocal =sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()