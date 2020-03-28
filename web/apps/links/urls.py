from django.urls import path

from links import views

urlpatterns = [
    path('', views.links_view),
    path('json', views.links_json)
]
