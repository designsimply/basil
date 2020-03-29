from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('links.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('.sadmin/', admin.site.urls),
]
