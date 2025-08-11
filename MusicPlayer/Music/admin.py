from django.contrib import admin

from Music.models import Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'image', 'duration')
    list_filter = ('title', 'artist')
    search_fields = ('title', 'artist')
