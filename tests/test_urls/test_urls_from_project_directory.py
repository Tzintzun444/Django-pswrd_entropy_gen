from pswrd_entropy_gen.views import IndexView, DocumentationView
from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import pytest


@pytest.mark.parametrize('url,args,url_name,view', [
    ('/', None, 'index', IndexView),
    ('/api/token/', None, 'obtain_token', TokenObtainPairView),
    ('/api/token/refresh/', None, 'refresh_token', TokenRefreshView),
    ('/docs/v1.0.2/', ['v1.0.2'], 'docs', DocumentationView),
    ('/docs/v2.0.0/', ['v2.0.0'], 'docs', DocumentationView),
    ('/docs/latest/', ['latest'], 'docs', DocumentationView)
])
def test_users_urls_with_reverse_and_resolve(url, args, url_name, view):

    url_from_reverse = reverse(url_name, args=args)

    assert url_from_reverse == url

    match = resolve(url)

    assert match.view_name == url_name
    assert match.func.view_class == view
