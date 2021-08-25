import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestMoviePage:
    def test_existing_news(self, client, news_factory):
        news = news_factory
        response = client.get(reverse('news.single_news', kwargs=dict(news_id=news.id)))
        assertTemplateUsed(response, 'news/single_news_page.html')
        assert response.status_code == 200

    def test_not_existing_news(self, client, news_factory):
        news = news_factory

        assert client.get(reverse('news.single_news', kwargs=dict(news_id=news.id + 1))).status_code == 404
