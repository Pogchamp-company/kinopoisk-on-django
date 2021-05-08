from django.shortcuts import render


def http404_page_not_found(request, *args, **kwargs):
    return render(request, 'errors/404.html', status=404)
