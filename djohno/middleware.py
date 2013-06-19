from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode

_HTML_TYPES = ('text/html', 'application/xhtml+xml')


def replace_insensitive(string, target, replacement):
    """
    Similar to string.replace() but is case insensitive code borrowed
    from Django Debug Toolbar.
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]

    # no results so return the original string
    return string


class DjohnoMiddleware(object):
    tag = '</body>'

    def get_djohno(self):
        return render_to_string('djohno/_djohno_dose.html',
                                {'STATIC_URL': settings.STATIC_URL})

    def process_response(self, request, response):
        if not request.user.is_superuser:
            return response

        if not request.path.startswith(reverse('djohno_index')):
            return response

        if 'gzip' in response.get('Content-Encoding', ''):
            return response

        content_type = response.get('Content-Type',
                                    '').split(';')[0]

        if content_type not in _HTML_TYPES:
            return response

        response.content = replace_insensitive(
            smart_unicode(response.content),
            self.tag,
            smart_unicode(self.get_djohno() + self.tag)
        )

        if 'Content-Length' in response:
            response['Content-Length'] = len(response.content)

        return response
