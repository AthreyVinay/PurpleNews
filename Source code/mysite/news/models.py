from django.db import models

# Create your models here.

class Message(models.Model):
    message = models.CharField(max_length=200)

    def __str__(self):              # __unicode__ on Python 2
        return self.message


class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=800)
    country = models.CharField(max_length=20)
    category = models.CharField(max_length=15)
    keywords = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Tweet(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=200)
    article_id = models.ForeignKey('Article')

    def __str__(self):
        return self.text