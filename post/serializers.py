from rest_framework import serializers

from post.models import Post, Subscriber, SubscriberFollower


class PostBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class SubscriberBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'


class SubscriberFollowerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberFollower
        fields = '__all__'


class SubscriberFollowerRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberFollower
        fields = ['id', 'name']


class SubscriberRetrieveSerializer(serializers.ModelSerializer):
    followers = SubscriberFollowerRetrieveSerializer(many=True, read_only=True, source='prefetch_followers')

    class Meta:
        model = Subscriber
        fields = ['id', 'name', 'followers']


class PostRetrieveSerializer(serializers.ModelSerializer):
    subscribers = SubscriberRetrieveSerializer(many=True, read_only=True, source='prefetch_subscribers')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'subscribers']
