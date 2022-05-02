from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TweetLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
	parent = models.ForeignKey("self", related_name="retweet",
		null=True,
	 	on_delete=models.SET_NULL
	)
	author = models.ForeignKey(User, related_name="author",
		on_delete=models.CASCADE
	)
	title = models.CharField(max_length = 255)
	content = models.TextField(max_length=999)
	image = models.FileField(upload_to="images/", 
		blank=True, null=True
	)
	likes = models.ManyToManyField(User, 
		related_name="user_like", blank=True
	)

	def __str__(self):
		return str(self.content)