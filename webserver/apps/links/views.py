from django.shortcuts import render

from links import models


def links_view(request):
    links = models.Link.objects.all()
    context = {
        'links': links,
    }
    return render(request, 'links/links_view.html', context)
