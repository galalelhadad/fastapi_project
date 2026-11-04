import pytest


from app import models



@pytest.fixture
def test_vote(test_user,session,test_posts):
    post_vote = models.Vote(
    post_id=test_posts[3].id,
    user_id=test_user["id"]
)
    session.add(post_vote)
    session.commit()

def test_vote_exixt_post(authorized_client,test_posts):
    res=authorized_client.post("/votes/",json={"post_id":test_posts[3].id,"dir":1})
    assert res.status_code==201
def test_vote_non_exixt_post(authorized_client,test_posts):
    res=authorized_client.post("/votes/",json={"post_id":8000,"dir":1})
    assert res.status_code==404
def test_vote_exixt_post_with_votes(authorized_client,test_posts,test_vote):
    res=authorized_client.post("/votes/",json={"post_id":test_posts[3].id,"dir":1})
    assert res.status_code==409
def test_un_vote_exixt_post_with_votes(authorized_client,test_posts,test_vote):
    res=authorized_client.post("/votes/",json={"post_id":test_posts[3].id,"dir":0})
    assert res.status_code==204
def test_vote_unauthorized_exixt_post(client,test_posts):
    res=client.post("/votes/",json={"post_id":test_posts[3].id,"dir":1})
    assert res.status_code==401