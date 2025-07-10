from django.urls import reverse
import pytest


def test_documentation_view_renders(client):

    response = client.get(reverse('docs', args=['latest']))
    context = response.context

    assert response.status_code == 200
    assert 'docs.html' in [t.name for t in response.templates]
    assert 'html_content' in context
    assert 'version' in context
    assert 'allowed_versions' in context


@pytest.mark.parametrize('args,code', [
    (['latest'], 200),
    (['v1.0.2'], 200),
    (['v2.0.0'], 200),
    (['v17.9.9'], 404)
])
def test_documentation_view_codes(args, code, client):

    response = client.get(reverse('docs', args=args))

    assert response.status_code == code
