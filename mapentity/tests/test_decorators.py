import mock
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import PermissionDenied


from mapentity import app_settings
from mapentity.decorators import view_permission_required


class ViewPermissionRequiredTestCase(TestCase):
    def setUp(self):
        # Fake request and its positional and keywords arguments.
        self.request = mock.MagicMock()
        self.request.user.is_anonymous = mock.MagicMock(return_value=False)
        self.request_args = ['fake_arg']
        self.request_kwargs = {'fake': 'kwarg'}
        self.mocked_view = mock.MagicMock()

    def run_decorated_view(self):
        """Setup, decorate and call view, then return response."""
        decorated_view = view_permission_required()(self.mocked_view)
        # Return response.
        return decorated_view(self.mocked_view,
                              self.request,
                              *self.request_args,
                              **self.request_kwargs)

    def test_anonymous_are_redirected_to_login(self):
        self.request.user.is_anonymous.return_value = True
        self.request.user.has_perm.return_value = False
        response = self.run_decorated_view()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].startswith(settings.LOGIN_URL))

    def test_unauthorized_is_rendered_if_missing_perm(self):
        self.request.user.is_anonymous.return_value = False
        self.request.user.has_perm.return_value = False
        self.assertRaises(PermissionDenied, self.run_decorated_view)

    def test_permission_is_taken_from_view(self):
        self.request.user.is_anonymous.return_value = False
        self.mocked_view.get_view_perm.return_value = 'view-perm'
        self.run_decorated_view()
        self.request.user.has_perm.assert_called_once_with('view-perm')

    def test_anonymous_may_be_authorized_from_settings(self):
        self.request.user.is_authenticated.return_value = False
        self.mocked_view.get_view_perm.return_value = 'view-perm'
        app_settings['ANONYMOUS_VIEWS_PERMS'] = ('view-perm',)
        response = self.run_decorated_view()
        self.assertNotEqual(response.status_code, 200)
