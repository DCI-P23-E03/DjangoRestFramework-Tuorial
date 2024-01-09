from collections.abc import Iterable
from django.db import models
from django.utils.html import escape,strip_tags
from django.utils.text import slugify
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateField()
    is_published = models.BooleanField(default=False)

    
    