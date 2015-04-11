from django.core.urlresolvers import reverse
import djohno
from mock import Mock, patch
from tests.utils import DjohnoBaseViewTests


class DjohnoVersionViewTests(DjohnoBaseViewTests):
    def test_djohno_version_frame_with_login(self):
        """
        Tests to ensure loading the djohno framed app versions view is
        successful, and renders a few specific strings.
        """

        url = reverse('djohno_frame_versions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Djohno: Versions')
        self.assertContains(response,
                            'src="%s"' % reverse('djohno_versions'))

    def test_djohno_versions_with_login(self):
        """
        Tests to ensure loading the djohno versions view is
        successful.
        """
        def fake_get_pypi(app):
            if app == 'djohno':
                return djohno.__version__

            return '4.2'

        with patch('djohno.utils.get_pypi_version',
                   Mock(side_effect=fake_get_pypi)):
            url = reverse('djohno_versions')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response,
                                '<td class="fresh">Djohno</td>',
                                html=True)
            self.assertContains(response,
                                '<td>%s</td>' % djohno.__version__,
                                html=True)
            self.assertContains(response,
                                '<td class="stale">Django</td>',
                                html=True)
            self.assertContains(response,
                                '<td>4.2</td>',
                                html=True)
            self.assertContains(response,
                                '<tr class="version">',
                                count=4)
