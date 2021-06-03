from django.urls import path

from . import views

urlpatterns = [
    path("", views.GitHubForkView.as_view()),
    path("github/auth/", views.GithubAuthView.as_view()),
    path("fork", views.github_redirect)
]