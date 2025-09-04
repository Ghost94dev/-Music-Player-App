from django import forms
from Music.models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist','image','audio_file','lyrics', 'duration']
        
def clean_audio_file(self):
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file:
            # Check file size (10MB limit)
            if audio_file.size > 10 * 1024 * 1024:
                raise ValidationError("Audio file too large (max 10MB)")
        return audio_file
    
def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image file too large (max 5MB)")
        return image

    
