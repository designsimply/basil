from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('links.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('.sadmin/', admin.site.urls),
]


# This helper function works only in debug mode and only if the given prefix
# is local (e.g. /static/) and not a URL (e.g. http://static.example.com/).
# https://docs.djangoproject.com/en/3.0/howto/static-files/
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT,
)
