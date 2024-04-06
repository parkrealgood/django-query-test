import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from post.models import Post, Subscriber, SubscriberFollower


def create_post():
    posts = []
    for _ in range(10):
        posts.append(baker.make(Post))
    return posts


def create_subscriber(posts):
    subscribers = []
    for post in posts:
        subscribers.append(baker.make(Subscriber, post=post))
        subscribers.append(baker.make(Subscriber, post=post))
    return subscribers


def create_subscriber_follower(subscribers):
    followers = []
    for subscriber in subscribers:
        followers.append(baker.make(SubscriberFollower, subscriber=subscriber))
        followers.append(baker.make(SubscriberFollower, subscriber=subscriber))
        followers.append(baker.make(SubscriberFollower, subscriber=subscriber))
    return followers


@pytest.mark.django_db(databases="__all__")
class TestPostModel:

    def SetUp(self):
        self.posts = create_post()
        self.subscribers = create_subscriber(self.posts)
        self.followers = create_subscriber_follower(self.subscribers)

    def test_포스트_목록_조회(self):
        posts = create_post()
        subscribers = create_subscriber(posts)
        followers = create_subscriber_follower(subscribers)

        client = APIClient()
        res = client.get('/post/post/')
        assert res.status_code == 200
        result = res.json()
