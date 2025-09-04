from django.db import models
import json, ast
from cloudinary.models import CloudinaryField
# Create your models here.

class Song(models.Model):
    title = models.TextField()
    artist = models.TextField()
    image = CloudinaryField('image')
    audio_file = CloudinaryField(resource_type='video')
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

    @property
    def secure_image_url(self):
        """Returns the image URL with HTTPS"""
        if self.image:
            url = self.image.url
            if url.startswith('http://'):
                return url.replace('http://', 'https://', 1)
            return url
        return None

    @property
    def secure_audio_url(self):
        """Returns the audio URL with HTTPS"""
        if self.audio_file:
            url = self.audio_file.url
            if url.startswith('http://'):
                return url.replace('http://', 'https://', 1)
            return url
        return None

