from django.urls import path

from tweet.views import (TweetListViewApi,
      TweetUpdateView,
      TweetDeleteView,
      TweetDetailView,
      TweetActionView
)

urlpatterns = [
    path('', TweetListViewApi.as_view(), name="tweet"),
    path('<int:tweet_id>/', TweetDetailView.as_view(), name="tweet_detail"),
    path('<int:tweet_id>/update/', TweetUpdateView.as_view(), name="tweet_update"),
    path('<int:tweet_id>/delete/', TweetDeleteView.as_view(), name="tweet_update"),
    path('<int:tweet_id>/action/', TweetActionView.as_view(), name="tweet_action"),
]
