from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.views import View
from django.http import HttpRequest
import requests
from requests.status_codes import codes
from pprint import pformat
# Create your views here.

def github_redirect(request):
    base = "https://github.com/login/oauth/authorize"
    scope = 'public_repo'
    url = f"{base}?client_id={settings.GITHUB_CLIENT_ID}&scope={scope}"
    response = redirect(url)
    return response


class GitHubForkView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'repo_owner': settings.GITHUB_REPO_OWNER,
            'repo_name': settings.GITHUB_REPO_NAME,
            'repo_url': request.GET.get('repo_url'),
        }
        return render(request, 'core/fork_repo.html', context)


class GithubAuthView(View):

    def get(self, request, *args, **kwargs):
        ''' '''
        code = request.GET.get('code')
        if not code:
            return HttpResponse('No code')

        access_resp = self.request_github_access(code)
        try:
            access_resp.json()
        except:
            return HttpResponse("Error requesting token: " + access_resp.text)

        if token := access_resp.json().get('access_token'):
            return self.handle_fork(request, token)

        elif errors := access_resp.json().get('error'):
            return self.handle_errors(request, errors)

        return HttpResponse("Unknown response has neither token nor errors: " + pformat(access_resp.json()))

    def request_github_access(self, code):
        resp = requests.post(settings.GITHUB_AUTH_URL,
            data={
                'client_id': settings.GITHUB_CLIENT_ID,
                'client_secret': settings.GITHUB_CLIENT_SECRET,
                'code': code,
            },
            headers={'Accept': 'application/json'}
        )
        return resp

    def handle_fork(self, request, token):
        fork_resp = self.fork_repo(
            settings.GITHUB_REPO_OWNER,
            settings.GITHUB_REPO_NAME,
            token,
        )
        if fork_resp.status_code != codes.ACCEPTED:
            return HttpResponse(f"Cannot fork repo. Got status: {fork_resp.status_code}")
        base = '/'
        repo_url = fork_resp.json().get('html_url')
        url = f"{base}?repo_url={repo_url}"
        return redirect(url)

    def handle_errors(self, request, errors):
        return HttpResponse("Errors requsting token: " + pformat(errors))

    def fork_repo(self, owner, name, token):
        return fork_repo(owner, name, token)


def fork_repo(owner, name, token):
    headers = {
        "Authorization": f"token {token}",
    }
    headers.update(settings.GITHUB_HEADERS)

    base_url = settings.GITHUB_BASE_URL
    url = f"{base_url}/repos/{owner}/{name}/forks"

    resp = requests.post(url, headers=headers)
    return resp
