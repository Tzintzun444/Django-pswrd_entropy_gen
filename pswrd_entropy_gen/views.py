from django.views.generic import TemplateView
from django.utils.translation import get_language, gettext_lazy as _
from django.http import Http404
from django.conf import settings
from pathlib import Path
import markdown
import os


class IndexView(TemplateView):

    template_name = 'index.html'


class DocumentationView(TemplateView):

    template_name = 'docs.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        language = get_language()
        version = kwargs['version']

        allowed_versions = ['v1.0.2', 'v2.0.0', 'latest']
        allowed_versions.sort(reverse=True)
        languages = ['en']

        if version not in allowed_versions or language not in languages:

            raise Http404(_('This version or language is not available or does not exist'))

        if version == 'latest':

            md_path = Path(os.path.join(
                settings.BASE_DIR,
                f'static/documentation/{allowed_versions[0]}/{language}/README.md'))

        else:

            md_path = Path(os.path.join(settings.BASE_DIR, f'static/documentation/{version}/{language}/README.md'))

        md_raw = md_path.read_text(encoding='utf-8')
        md_raw = md_raw.replace('entropy_formula.png', '/static/images/entropy_formula.png')
        md_raw = md_raw.replace('decryption_time_formula.png', '/static/images/decryption_time_formula.png')

        html = markdown.markdown(md_raw, extensions=[
            'fenced_code',
            'codehilite',
            'tables',
            'sane_lists',
        ])
        context['html_content'] = html
        context['version'] = version

        allowed_versions.remove('latest')
        context['allowed_versions'] = ['latest'] + allowed_versions

        return context
