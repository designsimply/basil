from django.urls import path

from links import views

urlpatterns = [
    path('links', views.links_view),
]
