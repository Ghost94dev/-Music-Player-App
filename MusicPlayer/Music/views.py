from django.shortcuts import render
from django.http import HttpResponse
from Music.models import Song
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    return HttpResponse("Hello, World!")


def index(request):
    paginator = Paginator(Song.objects.all().order_by('id'), 1)  # Added ordering
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Debug output - check in your server console
    for song in page_obj:
        print("Lyrics data:", song.lyrics)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "index.html", context)
