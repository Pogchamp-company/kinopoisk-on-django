from django.shortcuts import render
from django.templatetags.static import static


def http404_page_not_found(request, *args, **kwargs):
    return render(request,
                  'errors/base_error.html',
                  context=dict(video=static('media/errors/404.mp4'),
                               error_message='Error 404: Page not found'),
                  status=404)


def http500_internal_server_error(request, *args, **kwargs):
    return render(request,
                  'errors/base_error.html',
                  context=dict(video=static('media/errors/500.mp4'),
                               error_message='Error 500: Internal Server Error'),
                  status=500)
