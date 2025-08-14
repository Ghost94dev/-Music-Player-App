from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse
from Music.models import Song
from django.core.paginator import Paginator
import syncedlyrics
import re
import json
from Music.forms import SongForm
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q

# Create your views here.

def home(request):
    return HttpResponse("Hello, World!")


def index(request):
    song_id = request.GET.get("song_id")

    if song_id:  # Directly load one song
        song = get_object_or_404(Song, id=song_id)
        page_obj = [song]
        total_page = 1

        context = {
            "page_obj": page_obj,
            "total_page": total_page,
        }
        return render(request, "index.html", context)

    else:
        paginator = Paginator(Song.objects.all().order_by("id"), 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        total_page = paginator.num_pages


        for song in page_obj:
            print("Lyrics data:", song.lyrics)

        context = {
            "page_obj": page_obj,
            "total_page": paginator.num_pages,  # Pass total number of pages
        }
        return render(request, "index.html", context)



def song_list(request):
    query = request.GET.get('q', '')  # search term from URL
    songs = Song.objects.all().order_by("id")

    if query:
        songs = songs.filter(
            Q(title__icontains=query) | Q(artist__icontains=query)
        )

    return render(request, "songs_list.html", {"songs": songs, "query": query})


def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save()  # Save and store the instance in `song`
            return redirect(f"{reverse('music:index')}?song_id={song.id}")
    else:
        form = SongForm()

    return render(request, 'add_song.html', {'form': form})


def get_lyrics(request):
    lyrics_json = None
    query = request.GET.get("query")
    if query:
        lrc = syncedlyrics.search(query)
        pattern = r'\[(\d+:\d+\.\d+)\] (.+)'
        json_data = []
        for line in lrc.split('\n'):
            match = re.match(pattern, line)
            if match:
                timestamp, text = match.groups()
                json_data.append({"time": timestamp, "lyrics": text})
        lyrics_json = json.dumps(json_data, indent=4)
    return render(request, "get_lyrics.html", {"lyrics_json": lyrics_json})