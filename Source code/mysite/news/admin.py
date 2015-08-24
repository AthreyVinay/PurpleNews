from django.contrib import admin
from .models import Article, Tweet

# Register your models here.

admin.site.register(Article)
admin.site.register(Tweet)