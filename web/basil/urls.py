from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('helloworld.urls')),
    path('links', include('links.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('.sadmin/', admin.site.urls),
]
