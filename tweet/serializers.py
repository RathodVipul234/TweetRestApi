from rest_framework import serializers
from django.contrib.auth.models import User
from tweet.models import Tweet, TweetLike
from django.shortcuts import get_object_or_404
from django.core import serializers as json_serializers


class TweetSerializers(serializers.ModelSerializer):
    class Meta:
        """ Meta class"""
        model = Tweet
        fields = ['id', 'title', 'content', 'image']

        extra_kwargs = {
            "title": {"required": True },
            "content": {"required": True },
        }

    def create(self, validated_data):
        """Create Tweet object with create method"""
        user = get_object_or_404(User,id=self.context.get("request").user.id)
        tweet = self.context.get("tweet") if self.context.get("tweet") else None
        return Tweet.objects.create(author= user,
            parent = tweet,
            **validated_data
        )


    def validate_content(self, content):
        """validate serializers"""
        if len(content) > 200:
            raise serializers.ValidationError("Tweet id too long!")

        return content


class TweetDetailSerializers(serializers.ModelSerializer):
    """Tweet serializers """
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetSerializers(read_only=True)
    class Meta:
        """ Meta class"""
        model = Tweet
        fields = ['id', 'title', 'content', 'image', 'likes', 'parent']

        extra_kwargs = {
            "title": {"read_only": True },
            "content": {"read_only": True },
            "parent": {"read_only": True }
        }


    def get_likes(self, obj):
        return obj.likes.all().count()


class TweetActionSerializer(serializers.Serializer):
    """Tweet action serializers"""
    action = serializers.CharField()

    def validate_action(self, action):
        """validate action"""
        if not action.lower().strip() in ['like', 'dislike', 'retweet']:
            raise serializers.ValidationError(
                "this is not valid action on tweet!"
            )
        return action
