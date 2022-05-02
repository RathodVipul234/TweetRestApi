from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import UpdateAPIView, DestroyAPIView, RetrieveAPIView

from tweet.models import Tweet, TweetLike
from tweet.serializers import TweetSerializers, TweetActionSerializer, TweetDetailSerializers

# Create your views here.

class TweetListViewApi(APIView):
    """Tweet serializers"""
    serializer_class = TweetSerializers
    serializer_details_class = TweetDetailSerializers

    def get(self, request, *args, **kwrags):
        """
            get list of all tweets
        """
        tweets = Tweet.objects.all()
        serialize_data = self.serializer_details_class(tweets, many=True)

        return Response(serialize_data.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwrags):
        """
            save tweet method
        """
        data = request.data
        serializer = self.serializer_class(data=data,
            context={
                'request': self.request,
            }
        )

        if serializer.is_valid(raise_exception = True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, *args, **kwrags):
        """
            save tweet method
        """
        data = request.data
        serializer = self.serializer_class(data=data,
            context={
                'request': self.request,
            }
        )

        if serializer.is_valid(raise_exception = True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class TweetDetailView(RetrieveAPIView):
    """Tweet Detais"""

    serializer_class = TweetDetailSerializers
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.pop('tweet_id', False)
        obj = get_object_or_404(Tweet, pk=id)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class TweetUpdateView(UpdateAPIView):
    """Update Tweet view"""

    serializer_class = TweetSerializers

    def update(self, request, *args, **kwrags):
        id = kwrags.pop('tweet_id', False)
        obj = get_object_or_404(Tweet, pk=id)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TweetDeleteView(DestroyAPIView):
    """Delete tweet objects"""

    def destroy(self, request, *args, **kwargs):
        id =  kwargs.pop('tweet_id')
        obj = get_object_or_404(Tweet, pk=id)
        self.perform_destroy(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class TweetActionView(APIView):
    """ Like and Unlike Action view""" 
    serializer_class = TweetActionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwrags):
        """ like and dislike post method"""
        data = self.request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception = True):
            id = kwrags.pop('tweet_id', False)
            tweet_obj = get_object_or_404(Tweet, pk=id)
            action = serializer.validated_data.get("action")
            user = self.request.user
            if action == "like":
                tweet_obj.likes.add(user)
            elif action == "dislike":
                tweet_obj.likes.remove(user)
            elif action == "retweet":
                # data = {
                #     "user": self.request.user,
                #     "parent":tweet_obj,

                # }
                data = self.request.data
                serializer = TweetSerializers(data=data, context={
                    'request': self.request,
                    'tweet' : tweet_obj
                })

                if serializer.is_valid(raise_exception = True):
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            tweet_obj.save()
            tweet_serializers = TweetSerializers(tweet_obj)
        return Response(tweet_serializers.data, status=status.HTTP_204_NO_CONTENT)
