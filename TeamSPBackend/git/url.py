from TeamSPBackend.common.github_util import get_commits
from django.urls import path

from TeamSPBackend.git.views import getCommits, listContribution, getLastCommit, updateCommits, getFileMetrics
from TeamSPBackend.git.views import getUpdates

urlpatterns = [
    path('updateCommits', updateCommits),
    path('getCommits', getCommits),
    path('listContribution', listContribution),
    path('getLastCommit', getLastCommit),
    path('getFileMetrics', getFileMetrics),
    path('getUpdates',getUpdates),
]

