# Generated by Django 4.0.3 on 2022-04-14 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0004_remove_tweet_likes_tweet_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.TextField(blank=True, default='testing'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tweet',
            name='title',
            field=models.CharField(default='testing', max_length=255),
            preserve_default=False,
        ),
    ]