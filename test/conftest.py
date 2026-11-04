from fastapi.testclient import TestClient
from app.main import app


from sqlalchemy import create_engine,URL
from sqlalchemy.orm import sessionmaker , declarative_base
from app.config import settings
from app.database import Base,get_db
import pytest
from app.outh2 import create_access_token
from app import models
SQLALCHEMY_DATABASE_URL=f"postgresql+psycopg2://{settings.database_username}:{settings.database_password
        }@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


engine=create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionlocal =sessionmaker(autocommit=False,autoflush=False,bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db        
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data={"email":"galalglgl@gmail.com",
               "password":"password123"
    }
    res=client.post("/users/",json=user_data)
    new_user=res.json()
    assert res.status_code==201
    new_user['password']=user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data={"email":"RAHMA@gmail.com",
               "password":"password123"
    }
    res=client.post("/users/",json=user_data)
    new_user=res.json()
    assert res.status_code==201
    new_user['password']=user_data["password"]
    return new_user

@pytest.fixture
def test_token(test_user):
    token=create_access_token({'user_id':test_user['id']})
    return token

@pytest.fixture
def authorized_client(test_token,client):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {test_token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,test_user2,session):
    post_data=[
            {
                "title":"1st post",
                "content":"1st content",
                "owner_id":test_user['id']
            },
            {
                "title":"2ND post",
                "content":"2ND content",
                "owner_id":test_user['id']
            },

            {
                "title":"3RD post",
                "content":"3RD content",
                "owner_id":test_user['id']
            },
            {
                "title":"4TH post",
                "content":"4TH content",
                "owner_id":test_user2['id']
            },
    ]
    def create_post_model(post_dict):
        post=models.Post(**post_dict)
        return post
    map_post=map(create_post_model,post_data)
    session.add_all(list(map_post))
    session.commit()
    posts=session.query(models.Post).all()
    return posts




