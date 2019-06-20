from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class Post(models.Model):
    image = ProcessedImageField(
        upload_to='images/',

        processors=[Thumbnail(600, 600)],
        format='JPEG',
        options={'quality': 90},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


