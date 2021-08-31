from TeamSPBackend.common.github_util import get_commits
from django.urls import path
from TeamSPBackend.git.views import getCommits

urlpatterns = [
    path('getCommits/',getCommits),
]