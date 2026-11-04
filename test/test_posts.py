import pytest
from app import schemas


def test_get_all_posts(authorized_client,test_posts):
    res=authorized_client.get("/posts/")
    assert len(res.json())==len(test_posts)
    assert res.status_code==200


def test_unouthorized_client_get_all_posts(client,test_posts):
    res=client.get("/posts/")

    assert res.status_code==401
    

def test_authorized_client_get_one_exist_post(authorized_client,test_posts):
    res=authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.json().get("title")==test_posts[0].title
    assert res.status_code==200

def test_authorized_client_get_one_non_exist_post(authorized_client,test_posts):
    res=authorized_client.get(f"/posts/8000")
    assert res.status_code==404

def test_un_authorized_client_get_one_post(client,test_posts):
    res=client.get(f"/posts/8000")
    assert res.status_code==401
@pytest.mark.parametrize("title,content,published",{
    ("first post","frist content",True),
    ("jghgh","hfhgdg",False),
    ("3rd post","3rd content",True)

})
def test_craete_post(authorized_client,title,content,published):
    res=authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    create_post=schemas.CreatePost(**res.json())
    assert res.json().get("title")==title
    assert res.json().get("content")==content
    assert res.json().get("published")==published
    assert res.status_code==201


def test_craete_post_default_publisshed(authorized_client):
    res=authorized_client.post("/posts/",json={"title":"jfjfjf","content":"content"})
    create_post=schemas.CreatePost(**res.json())
    assert res.json().get("title")=="jfjfjf"
    assert res.json().get("content")=="content"
    assert res.json().get("published")==True
    assert res.status_code==201

def test_unauthorized_client_craete_post(client):
    res=client.post("/posts/",json={"title":"jfjfjf","content":"content"})
   
    assert res.status_code==401

def test_authorized_client_delete_post(authorized_client,test_posts):
    res=authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code==204

def test_unauthorized_client_delete_post(client,test_posts):
    res=client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code==401

def test_authorized_client_delete_other_post(authorized_client,test_posts):
    res=authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code==403

def test_authorized_client_delete_non_exist_post(authorized_client,test_posts):
    res=authorized_client.delete(f"/posts/8000")
    assert res.status_code==404

def test_update_exist_post(authorized_client,test_posts):
    res=authorized_client.put(f"posts/{test_posts[0].id}",json={"title":"jfjfjf","content":"content"})
    assert res.json().get('title')=="jfjfjf"
    assert res.status_code==200

def test_update_NON_exist_post(authorized_client,test_posts):
    res=authorized_client.put(f"posts/8000",json={"title":"jfjfjf","content":"content"})
    assert res.status_code==404


def test_un_authorized_update_exist_post(client,test_posts):
    res=client.put(f"posts/{test_posts[0].id}",json={"title":"jfjfjf","content":"content"})

    assert res.status_code==401


def test_update_other_exist_post(authorized_client,test_posts):
    res=authorized_client.put(f"posts/{test_posts[3].id}",json={"title":"jfjfjf","content":"content"})

    assert res.status_code==403



