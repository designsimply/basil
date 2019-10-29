from django.http import HttpResponse


def helloworld(request):
    return HttpResponse("Hello sheri!")


# from django.shortcuts import render
# def helloworld(request):
#     context = {
#         'var1': 'sheri',
#     }
#     return render(request, 'helloworld/index.html', context)
