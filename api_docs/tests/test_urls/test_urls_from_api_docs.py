from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import reverse, resolve
import pytest


@pytest.mark.parametrize('url,url_name,view', [
    ('schema/', 'schema', SpectacularAPIView),
    ('schema/swagger-ui/', 'swagger', SpectacularSwaggerView),
    ('schema/redoc/', 'redoc', SpectacularRedocView)
])
def test_users_urls_with_reverse_and_resolve(url, url_name, view):
    url = '/api/docs/' + url
    url_from_reverse = reverse(url_name)

    assert url_from_reverse == url

    match = resolve(url)

    assert match.view_name == url_name
    assert match.func.view_class == view
