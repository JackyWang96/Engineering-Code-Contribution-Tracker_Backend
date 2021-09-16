from TeamSPBackend.common.github_util import get_commits
from django.urls import path
from TeamSPBackend.git.views import GetCommits, listContribution, getLastCommit, updateCommits

urlpatterns = [
    path('updateCommits', updateCommits),
    path('getCommits/<space_key>', GetCommits.as_view()),
    path('listContribution', listContribution),
    path('getLastCommit', getLastCommit),
]
