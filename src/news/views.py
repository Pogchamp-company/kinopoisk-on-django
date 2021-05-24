from django.shortcuts import render, get_object_or_404
from news.models import News


def single_news_page(request, news_id: int):
    context = dict(
        news=get_object_or_404(News, pk=news_id)
    )

    return render(request, 'news/single_news_page.html', context)
