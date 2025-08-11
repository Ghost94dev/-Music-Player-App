from django.urls import path
from Music import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "music"

urlpatterns = [
    path('', views.index, name='index'),

]
