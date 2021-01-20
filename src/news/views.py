from django.shortcuts import render
from movies.models import Movie


def index(request):
    context = dict(
        preview=Movie.objects.order_by("-id")[:3]
    )

    return render(request, 'home_page.html', context)
