from django.db import models
import json, ast
from cloudinary.models import CloudinaryField
# Create your models here.

class Song(models.Model):
    title = models.TextField()
    artist = models.TextField()
    image = CloudinaryField('image', folder='songs/images/')
    audio_file = CloudinaryField('raw', resource_type='raw', folder='songs/audio/')
    audio_link = models.CharField(max_length=200, null=True, blank=True)
    lyrics = models.TextField(default='[]')
    duration = models.CharField(max_length=20)
    paginator_by=2

    def get_lyrics_json(self):
        try:
            return json.loads(self.lyrics)
        except:
            return []


    def __str__(self):
        return self.title

