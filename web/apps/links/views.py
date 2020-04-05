import logging
import urllib

from django.shortcuts import render

from django.core import serializers
from django.http import HttpResponse
from django.conf import settings

from links import models

logger = logging.getLogger(__name__)


def paginate_queryset(queryset, page=0, per_page=settings.MAX_PER_PAGE):
    """ add limit and offset to queryset

    Parameters
    ----------
    queryset : django queryset
    page : int
        which page, none sets to page=0
    per_page : int
        number to display per page

    Returns
    -------
    int
        number total from the queryset before slice
    django queryset
        subset of the queryset

    """
    per_page = min(per_page, settings.MAX_PER_PAGE)
    per_page = max(per_page, 1)

    total = queryset.count()
    max_pages = (total // per_page)

    page = max(page, 0)
    page = min(page, max_pages)

    start = (page) * per_page
    end = min((page + 1) * per_page, total)

    queryset = queryset[start:end]
    return (total, start, end, queryset)


def links_search_view(request):
    logger.info('SEARCH!')
    queryset = models.Link.objects.all()

    get_params = dict(request.GET)

    query = ''
    query_parts = get_params.pop('s', [])
    if len(query_parts):
        query = '%20'.join(query_parts)
        if query != 'null':
            query = urllib.parse.unquote(query)
            queryset = queryset.filter(title__icontains=query)

    per_page = get_params.pop('per_page', [])
    if len(per_page):
        try:
            per_page = int(per_page[0])
        except ValueError:
            per_page = settings.MAX_PER_PAGE
    else:
        per_page = settings.MAX_PER_PAGE

    page_1 = get_params.pop('page', [])
    if len(page_1):
        try:
            page_0 = int(page_1[0]) - 1
        except ValueError:
            page_0 = 0
    else:
        page_0 = 0

    total, start, end, queryset = paginate_queryset(
        queryset, page=page_0, per_page=per_page)

    # TODO: If unknown GET parameters are passed, just ignore them.

    context = {
        'links': queryset,
        'links_meta': {
            'page': page_0 + 1,
            'total': total,
            'start': start,
            'end': end,
        },
    }

    if settings.DEBUG:
        context['debug'] = {
            'get': dict(request.GET),
            'post': dict(request.POST),
            'path': request.path,
            'query': query,
        }

    return render(request, 'links/links_search_view.html', context)


def links_json(request):
    links = models.Link.objects.all()
    data = serializers.serialize('json', links)
    return HttpResponse(data, content_type='application/json')
