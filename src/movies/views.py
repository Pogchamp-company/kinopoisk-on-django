from django.shortcuts import render


def movie_page(request, movie_id: int):
    return render(request, 'movie_page.html')
