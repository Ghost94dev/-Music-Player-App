from django import forms
from Music.models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist','image','audio_file','lyrics', 'duration']
