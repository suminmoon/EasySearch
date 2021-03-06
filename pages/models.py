from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import Thumbnail

class Table(models.Model):
    userID = models.TextField()
    productNO = models.TextField()
    lowPRICE = models.TextField()

class Post(models.Model):
    image = models.ImageField(
        upload_to='images/',

    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


