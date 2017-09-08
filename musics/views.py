from django.shortcuts import render

from musics.models import Music


# Create your views here.
def hello_view(request):
    musics = Music.objects.all()

    return render(request, 'hello_django.html', {
        'data': "Hello Django ",
        'musics': musics,
    })
