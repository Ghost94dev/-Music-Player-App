from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from Music.models import Song
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    return HttpResponse("Hello, World!")


def index(request):
    song_id = request.GET.get("song_id")

    if song_id:  # Directly load one song
        song = get_object_or_404(Song, id=song_id)
        page_obj = [song]       # Just put it in a list for template compatibility
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

        # Debug output - check in your server console
        for song in page_obj:
            print("Lyrics data:", song.lyrics)

        context = {
            "page_obj": page_obj,
            "total_page": paginator.num_pages,  # Pass total number of pages
        }
        return render(request, "index.html", context)



def song_list(request):
    songs = Song.objects.all().order_by("id")  # Get all songs
    return render(request, "songs_list.html", {"songs": songs})
