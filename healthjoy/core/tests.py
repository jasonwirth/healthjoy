from unittest import mock
from django.test import TestCase
from django.test import Client
from unittest.mock import patch, Mock
from core.views import GithubAuthView
from requests import Response
# Create your tests here.


@patch.object(GithubAuthView, 'request_github_access')
class TestForkingRepo(TestCase):

    def auth_mock(self, config=None):
        resp = Mock(name='github_auth_response', spec=Response)
        if config:
            resp.configure_mock(**config)
        return resp

    def fork_mock(self, config=None):
        resp = Mock(name='github_fork_response', spec=Response)
        if config:
            resp.configure_mock(**config)
        return resp

    def test_accessed_without_code(self, *args):
        client = Client()
        response = client.get('/github/auth/')
        self.assertContains(response, 'No code')

    def test_got_token_and_repo_is_forked(self, request_github_access):
        request_github_access.return_value = self.auth_mock({
            'json.side_effect': lambda *args, **kwargs: {'access_token': '123456789'}
        })

        fork_resp = self.fork_mock({
            'status_code': 202,
            'json': lambda *args, **kwargs: {'html_url': 'http://github.com/my_fork/'}
        })

        with patch('core.views.fork_repo', return_value=fork_resp):

            client = Client()
            response = client.get('/github/auth/?code=githubcode')
            self.assertRedirects(response, '/?repo_url=http://github.com/my_fork/')

    def test_got_token_but_fork_fails(self, request_github_access):
        request_github_access.return_value = self.auth_mock({
            'json.side_effect': lambda *args, **kwargs: {'access_token': '123456789'}
        })

        fork_resp = self.fork_mock({
            'status_code': 404,
            'json': lambda *args, **kwargs: {'html_url': 'http://github.com/my_fork/'}
        })

        with patch('core.views.fork_repo', return_value=fork_resp):
            client = Client()
            response = client.get('/github/auth/?code=githubcode')
            self.assertContains(response, 'Cannot fork repo. Got status: 404')

    def test_github_auth_returns_errors(self, request_github_access):
        request_github_access.return_value = self.auth_mock({
            'json.side_effect': lambda *args, **kwargs: {'error': 'no token'}
        })

        client = Client()
        response = client.get('/github/auth/?code=githubcode')
        self.assertContains(response, 'no token')

    def test_github_auth_doesnt_return_json(self, request_github_access):
        request_github_access.return_value = self.auth_mock({
            'json.side_effect': ValueError('No JSON'),
            'text': 'no JSON'
        })

        client = Client()
        response = client.get('/github/auth/?code=githubcode')
        self.assertContains(response, 'no JSON')

    def test_github_auth_returns_nothing(self, request_github_access):
        request_github_access.return_value = self.auth_mock({
            'json.side_effect': lambda *args, **kwargs: {}
        })

        client = Client()
        response = client.get('/github/auth/?code=githubcode')
        self.assertContains(response, 'Unknown response')