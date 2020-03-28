from django.shortcuts import render

from django.core import serializers
from django.http import HttpResponse

from links import models


def links_view(request):
    links = models.Link.objects.all()
    context = {
        'links': links,
    }
    return render(request, 'links/links_view.html', context)


def links_json(request):
    links = models.Link.objects.all()
    data = serializers.serialize('json', links)
    return HttpResponse(data, content_type='application/json')
