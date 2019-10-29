from django.shortcuts import render


def helloworld(request):
    context = {
        'var1': 'Variables!',
    }
    return render(request, 'helloworld/index.html', context)
