from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.encoding import smart_str


def replace_insensitive(string, target, replacement):
    """
    Similar to string.replace() but is case insensitive code borrowed
    from Django Debug Toolbar.
    """
    no_case = string.lower()
    index = no_case.index(target.lower())

    return string[:index] + replacement + string[index + len(target):]


class DjohnoMiddleware(object):
    def get_djohno(self):
        return render_to_string('djohno/_djohno_dose.html',
                                {'STATIC_URL': settings.STATIC_URL})

    def should_process_response(self, request, response):
        if not hasattr(request, 'user'):
            # We get here if middleware issues a redirect before the
            # AuthenticationMiddleware has run (e.g. to append a
            # slash). Since we can't check if the user is allowed to
            # view Djohno pages at this point, we'll just assume they
            # can't.
            return False

        if not request.user.is_superuser:
            # If your name's not down, you're not coming in.
            return False

        if not request.path.startswith(reverse('djohno_index')):
            # We only want to show the Djohno toolbar for URLs within
            # the Djohno app.
            return False

        if 'gzip' in response.get('Content-Encoding', ''):
            # If it's gzipped, I can't help you.
            return False

        return True

    def process_response(self, request, response):
        if not self.should_process_response(request, response):
            return response

        tag = '</body>'

        response.content = replace_insensitive(
            smart_str(response.content),
            tag,
            smart_str(self.get_djohno() + tag)
        )

        if 'Content-Length' in response:
            response['Content-Length'] = len(response.content)

        return response
