from django.contrib import admin
from tweet.models import Tweet, TweetLike

# Register your models here.

class TweetLikeAdmin(admin.TabularInline):
	# list_dispaly = ['user']
	model = TweetLike


class TweetModelAdmin(admin.ModelAdmin):
	inlines = [TweetLikeAdmin]
	list_dispaly = ['content', 'image']


admin.site.register(Tweet, TweetModelAdmin)