import pytest

from app import schemas
from jose import jwt
from app.config import settings
# from .database import client,session
# def test_root(client):
#     res=client.get("/")
#     assert res.json().get("message")=="hello world"
#     assert res.status_code==200

def test_create_user(client):
    res=client.post("/users/",json={"email":"galalglgl@gmail.com","password":"password123"})
    new_user=schemas.User(**res.json())
    assert new_user.email=="galalglgl@gmail.com"
    assert res.status_code==201


def test_login(test_user,client):

    res=client.post("/login/",json={"email":test_user['email'],"password":test_user['password']})
    test_token=schemas.Token(**res.json())
    paylpad_data=jwt.decode(test_token.token,settings.secret_key,settings.algorithm)
    id=paylpad_data.get("user_id")
    assert res.status_code==200
    assert test_token.token_type=="bearer"
    assert test_user['id']==id




@pytest.mark.parametrize("email,password,status_code",[
    (None,"password123",422),
    ("galalglgl@gmail.com",None,422),
    ("galalglgl@gmail.com","WRONG PASS",403),
    ("WRONG_EMAIL@gmail.com","password123",403)


])
def test_wrong_login(test_user,client,email,password,status_code):
    res=client.post("/login/",json={"email":email,"password":password})
    assert res.status_code==status_code