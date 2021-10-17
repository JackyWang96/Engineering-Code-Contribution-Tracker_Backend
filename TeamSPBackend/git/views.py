from django.shortcuts import render

# Create your views here.
from collections import defaultdict
from TeamSPBackend.common import utils

from django.views.decorators.http import require_http_methods
from requests.models import Response
from TeamSPBackend.git.models import StudentCommitCounts, GitCommitCounts, GitMetrics, GitCommit, FileMetrics, GitContribution, CommitChange
from TeamSPBackend.common import utils
from TeamSPBackend.common.github_util import get_commits, get_und_metrics
from TeamSPBackend.api.dto.dto import GitDTO
from TeamSPBackend.common.choices import RespCode
from TeamSPBackend.common.utils import make_json_response, check_user_login, body_extract, check_body, \
    init_http_response_my_enum
from TeamSPBackend.project.models import ProjectCoordinatorRelation
from TeamSPBackend.confluence.models import UserList
import time
import datetime
from TeamSPBackend.common.utils import transformTimestamp
import requests
import json
from django.http import JsonResponse, HttpResponse
from rest_framework import generics
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response


baseUrl = 'https://api.github.com/'


# class GetCommits(generics.ListAPIView):
#     """
#     Retrieve data from Resort table, depending on the Param of country_id in the request.
#     Possible used in: provider sign up step 2
#     """
#     serializer_class = CommitSerializer

#     def get_queryset(self):
#         space_key = self.kwargs['space_key']
#         return GitCommit.objects.filter(space_key=space_key)


def getToken(id, space_key):
    token = ProjectCoordinatorRelation.objects.get(
        coordinator_id=id, space_key=space_key).git_token
    return token


def getUserList(space_key):
    user = UserList.objects.filter(space_key=space_key)
    username = []
    for item in user:
        username.append(item.git_username)
    return username


def getOwnerRepo(id, space_key):
    frontend = ProjectCoordinatorRelation.objects.get(
        coordinator_id=id, space_key=space_key).git_url.split("/")
    backend = ProjectCoordinatorRelation.objects.get(
        coordinator_id=id, space_key=space_key).git_backend_url.split("/")
    list = []
    if len(backend) > 2:
        back = {
            "owner": backend[len(backend)-2],
            "repo": backend[len(backend)-1],
            "source": "backend"
        }
        list.append(back)
    if len(frontend) > 2:
        front = {
            "owner": frontend[len(frontend)-2],
            "repo": frontend[len(frontend)-1],
            "source": "frontend"
        }
        list.append(front)
    return list


def getFileMetrics(request, *args, **kwargs):
    json_body = json.loads(request.body)
    space_key = json_body.get("space_key")
    fileMetrics = FileMetrics.objects.filter(space_key=space_key)
    list = []
    for x in fileMetrics:
        dict = {
            "space_key": space_key,
            "source": x.source,
            "file_name": x.file_name,
            "CountDeclClass": x.CountDeclClass,
            "CountDeclExecutableUnit": x.CountDeclExecutableUnit,
            "CountLine": x.CountLine,
            "CountLineBlank": x.CountLineBlank,
            "CountDeclFunction": x.CountDeclFunction,
            "CountLineCode": x.CountLineCode,
            "CountLineCodeDecl": x.CountLineCodeDecl,
            "CountLineCodeExe": x.CountLineCodeExe,
            "CountLineComment": x.CountLineComment,
            "CountPath": x.CountPath,
            "CountStmt": x.CountStmt,
            "CountStmtDecl": x.CountStmtDecl,
            "CountStmtExe": x.CountStmtExe,
            "Cyclomatic": x.Cyclomatic,
            "Essential": x.Essential,
            "MaxNesting": x.MaxNesting,
            "RatioCommentToCode": x.RatioCommentToCode,
        }
        list.append(dict)
    return HttpResponse(json.dumps(list), content_type="application/json")


def updateCommits(request, *args, **kwargs):
    json_body = json.loads(request.body)
    space_key = json_body.get("space_key")
    coordinator_id = request.session.get('coordinator_id')
    doUpdate(coordinator_id, space_key)
    resp = init_http_response_my_enum(RespCode.success)
    return make_json_response(resp=resp)


def autoUpdateCommits():
    records = ProjectCoordinatorRelation.objects.all()
    for record in records:
        doUpdate(record.coordinator_id, record.space_key)


def doUpdate(coordinator_id, space_key):
    # try:
    coordinator_id = coordinator_id
    space_key = space_key
    token = getToken(coordinator_id, space_key)
    record = getOwnerRepo(coordinator_id, space_key)
    username = getUserList(space_key)
    shaRecord = GitCommit.objects.filter(space_key=space_key)
    for item in record:
        owner = item.get("owner")
        repo = item.get("repo")
        url = baseUrl + "repos/" + owner + "/" + repo + "/commits?per_page=150"
        content = requests.get(
            url=url, headers={'Authorization': 'Bearer ' + token})
        convert = json.loads(content.text)
        # list = []
        for x in convert:
            if GitCommit.objects.filter(sha=x.get("sha")).exists():
                continue
            if x is None or x.get("author") is None or x.get("author").get("login") not in username:
                continue
            msg = x.get("commit").get("message")
            if len(msg) > 500:
                msg = msg[0:500]+"..."
            commit = GitCommit.objects.create(
                space_key=space_key,
                sha=x.get("sha"),
                url=x.get("html_url"),
                username=x.get("author").get("login"),
                date=x.get("commit").get("author").get("date"),
                message=msg,
                source=item.get("source")
            )
            commit.save()

        # update changes to commit change table
        for sha in shaRecord:
            if CommitChange.objects.filter(sha=sha.sha).exists():
                continue
            url = baseUrl + "repos/" + owner + "/" + repo + "/commits/" + sha.sha
            content = requests.get(
                url=url, headers={'Authorization': 'Bearer ' + token})
            convert = json.loads(content.text)
            files = convert.get("files")
            if files is None:
                continue
            change = CommitChange.objects.create(
                sha=convert.get("sha"),
                date=sha.date,
                source=sha.source,
                space_key=sha.space_key,
                total=convert.get("stats").get("total"),
                additions=convert.get("stats").get("additions"),
                deletions=convert.get("stats").get("deletions"),
            )
            change.save()

        # update list contribution
        usernames = getUserList(space_key)
        url = baseUrl + "repos/" + owner + "/" + repo + "/stats/contributors"
        content = requests.get(
            url=url, headers={'Authorization': 'Bearer ' + token})
        convert = json.loads(content.text)
        for x in convert:
            commit = x.get("total")
            git_username = x.get("author").get("login")
            source = item.get("source")
            count = 0
            for number in x.get("weeks"):
                count = count + number.get("a") + number.get("d")
            if git_username not in usernames:
                continue
            username = UserList.objects.get(
                git_username=git_username).user_name
            if GitContribution.objects.filter(git_username=git_username, space_key=space_key, source=source).exists():
                GitContribution.objects.filter(
                    git_username=git_username, space_key=space_key, source=source).update(commit=commit, total=count)
            else:
                commit = GitContribution.objects.create(
                    commit=commit,
                    git_username=git_username,
                    username=username,
                    total=count,
                    space_key=space_key,
                    source=source
                )
                commit.save()
    resp = init_http_response_my_enum(RespCode.success)
    return make_json_response(resp=resp)


def getCommits(request, *args, **kwargs):
    json_body = json.loads(request.body)

    space_key = json_body.get("space_key")
    record = GitCommit.objects.filter(space_key=space_key)
    list = []
    for x in record:
        dict = {
            "date": x.date,
            "sha": x.sha,
            "author": x.username,
            "url": x.url,
            "message": x.message,
            "source": x.source,
        }
        list.append(dict)
    return HttpResponse(json.dumps(list), content_type="application/json")


def listContribution(request, *args, **kwargs):
    json_body = json.loads(request.body)
    coordinator_id = request.session.get('coordinator_id')
    space_key = json_body.get("space_key")
    list = []
    contributors = GitContribution.objects.filter(space_key=space_key)
    for user in contributors:
        dict = {
            "commits": user.commit,
            "username": user.username,
            "git_username": user.git_username,
            "space_key": user.space_key,
            "total": user.total,
            "source": user.source
        }
        list.append(dict)
    # return JsonResponse(list)
    return HttpResponse(json.dumps(list), content_type="application/json")

# changes in one commits


def getCommitChanges(request, *args, **kwargs):
    json_body = json.loads(request.body)
    coordinator_id = request.session.get('coordinator_id')
    space_key = json_body.get("space_key")
    record = getOwnerRepo(coordinator_id, space_key)
    list = []
    record = CommitChange.objects.filter(space_key=space_key)
    for item in record:
        total = {
            "date": item.date,
            "source": item.source,
            "total": item.total,
            "additions": item.additions,
            "deletions": item.deletions,
        }
        list.append(total)
    return HttpResponse(json.dumps(list), content_type="application/json")


def getLastCommit(request, *args, **kwargs):
    json_body = json.loads(request.body)
    coordinator_id = request.session.get('coordinator_id')
    space_key = json_body.get("space_key")
    token = getToken(coordinator_id, space_key)
    # record = getOwnerRepo(coordinator_id,space_key)
    contributor = GitContribution.objects.filter(space_key=space_key)
    names = []
    for item in contributor:
        names.append(item.git_username)
    list = []
    for x in names:
        name = x
        url = GitCommit.objects.filter(
            username=name, space_key=space_key)[0].url.split("/")
        apiUrl = baseUrl + "repos/" + \
            url[len(url)-4] + "/" + url[len(url)-3] + "/commits?author=" + name
        content = requests.get(
            url=apiUrl, headers={'Authorization': 'Bearer ' + token})
        # in some case the user changed their user name, this api will get a empty string
        # print(content.text=="[]")
        if content.text == "[]":
            continue
        convert = json.loads(content.text)[0]
        dict = {
            "url": convert.get("html_url"),
            "git_username": convert.get("commit").get("author").get("name"),
            "user": UserList.objects.get(git_username=name).user_name,
            "date": convert.get("commit").get("author").get("date"),
            "message": convert.get("commit").get("message")
        }
        list.append(dict)
    # return JsonResponse(list)
    return HttpResponse(json.dumps(list), content_type="application/json")


def update_individual_commits():
    for relation in ProjectCoordinatorRelation.objects.all():
        data = {
            "url": relation.git_url
        }
        # create GitDTO object
        git_dto = GitDTO()
        # extract body information and store them in GitDTO.
        body_extract(data, git_dto)

        if not git_dto.valid_url:
            resp = init_http_response_my_enum(RespCode.invalid_parameter)
            return make_json_response(resp=resp)
        git_dto.url = git_dto.url.lstrip('$')

        # request commits from  github api
        commits = get_commits(git_dto.url, relation.space_key, git_dto.author, git_dto.branch, git_dto.second_after,
                              git_dto.second_before)
        # commits = get_commits(git_dto.url, git_dto.author, git_dto.branch, git_dto.second_after, git_dto.second_before)
        if commits is None:
            resp = init_http_response_my_enum(RespCode.invalid_authentication)
            return make_json_response(resp=resp)
        if commits == -1:
            resp = init_http_response_my_enum(RespCode.user_not_found)
            return make_json_response(resp=resp)
        if commits == -2:
            resp = init_http_response_my_enum(RespCode.git_config_not_found)
            return make_json_response(resp=resp)
        CommitCount = defaultdict(lambda: 0)
        for commit in commits:
            CommitCount[commit['author']] += 1

        for key, value in CommitCount.items():

            if StudentCommitCounts.objects.filter(student_name=str(key)).exists():
                user = StudentCommitCounts.objects.get(student_name=str(key))
                if str(value) != user.commit_counts:
                    StudentCommitCounts.objects.filter(
                        student_name=str(key)).update(commit_counts=str(value))
            else:
                user = StudentCommitCounts(student_name=str(key), commit_counts=str(value),
                                           space_key=relation.space_key)
                user.save()


"""
Auto update git commits per day. 
And it's necessary to consider 3 cases:
1. Git_commit db has this space_key, so just update a new day data
2. It doesn't have, crawler data and sorted by date
3. Server crash, and in order to avoid duplication, don't do commit_query
"""


def auto_update_commits(space_key):
    today = transformTimestamp(time.time())
    # print("space_key is: "+str(space_key))
    # if space_key not None means user update their configuration, and it will update database at once
    if space_key is not None:
        if not GitCommitCounts.objects.filter(space_key=space_key).exists():
            if ProjectCoordinatorRelation.objects.filter(space_key=space_key).exclude(git_url__isnull=True).exists():
                relation = ProjectCoordinatorRelation.objects.filter(
                    space_key=space_key).exclude(git_url__isnull=True)[0]
                git_dto = construct_url(relation)
                if not git_dto.valid_url:
                    return
                commits = get_commits(git_dto.url, space_key, git_dto.author, git_dto.branch, git_dto.second_after,
                                      git_dto.second_before)
                first_crawler(commits, space_key)

    for relation in ProjectCoordinatorRelation.objects.all():
        space_key = relation.space_key
        # Case 3: avoid duplications
        if GitCommitCounts.objects.filter(space_key=space_key, query_date=today).exists():
            continue
        # construct dto
        git_dto = construct_url(relation)
        # not a valid url, continue
        if not git_dto.valid_url:
            continue
        commits = get_commits(git_dto.url, space_key, git_dto.author, git_dto.branch, git_dto.second_after,
                              git_dto.second_before)
        # exception handler
        if commits is None or commits == -1 or commits == -2:
            continue

        # Case 1: has space_key
        if GitCommitCounts.objects.filter(space_key=space_key).exists():
            count = len(commits)

            git_data = GitCommitCounts(
                space_key=space_key,
                commit_counts=count,
                query_date=today
            )
            git_data.save()

        # Case 2: the first crawler
        else:
            first_crawler(commits, space_key)


def construct_url(relation):
    data = {
        "url": relation.git_url
    }
    git_dto = GitDTO()
    body_extract(data, git_dto)
    git_dto.url = git_dto.url.lstrip('$')
    return git_dto


def first_crawler(commits, space_key):
    delta_commit_count = {}  # To store every day commit count
    days = []  # For a month loop
    today = transformTimestamp(time.time())
    for i in range(30):
        days.append(today - i * 24 * 60 * 60)

    for commit in commits:
        ts = commit['date']
        for i in days:
            if ts > i:
                break
            else:
                if i in delta_commit_count:
                    delta_commit_count[i] += 1
                else:
                    delta_commit_count[i] = 1

    days = [i for i in reversed(days)]  # sort low to high
    for day in days:
        count = 0
        if day in delta_commit_count:
            count = delta_commit_count[day]
        # data which are returned to front end
        tmp = {
            "time": int(day),
            "commit_count": int(count)
        }
        # store data into db by date
        git_data = GitCommitCounts(
            space_key=space_key,
            commit_counts=count,
            query_date=day
        )
        git_data.save()


def get_metrics(relation):
    data = {
        "url": relation.git_url
    }
    backendData = {
        "url": relation.git_backend_url
    }
    save_metrics(data, relation.space_key, "frontend")
    save_metrics(backendData, relation.space_key, "backend")


def save_metrics(data, space_key, source):
    # create GitDTO object
    git_dto = GitDTO()
    # extract body information and store them in GitDTO.
    body_extract(data, git_dto)
    if not git_dto.valid_url:
        resp = init_http_response_my_enum(RespCode.no_repository)
        return make_json_response(resp=resp)
    git_dto.url = git_dto.url.lstrip('$')
    metrics = get_und_metrics(git_dto.url, space_key, source)
    fileMetrics = sortTopTen(metrics[1:len(metrics)])

    if metrics is None:
        resp = init_http_response_my_enum(RespCode.invalid_authentication)
        return make_json_response(resp=resp)
    elif metrics == -1:
        resp = init_http_response_my_enum(RespCode.user_not_found)
        return make_json_response(resp=resp)
    elif metrics == -2:
        resp = init_http_response_my_enum(RespCode.git_config_not_found)
        return make_json_response(resp=resp)

    for file in fileMetrics:
        if FileMetrics.objects.filter(space_key=space_key, source=source, file_name=file["filename"]).exists():
            FileMetrics.objects.filter(space_key=space_key, source=source, file_name=file["filename"]).update(
                CountDeclClass=ifExist('CountDeclClass', file["attribute"]),
                CountDeclExecutableUnit=ifExist(
                    'CountDeclExecutableUnit', file["attribute"]),
                CountLine=ifExist('CountLine', file["attribute"]),
                CountLineBlank=ifExist('CountLineBlank', file["attribute"]),
                CountLineCode=ifExist('CountLineCode', file["attribute"]),
                CountLineCodeDecl=ifExist(
                    'CountLineCodeDecl', file["attribute"]),
                CountDeclFunction=ifExist(
                    'CountDeclFunction', file["attribute"]),
                CountLineCodeExe=ifExist(
                    'CountLineCodeExe', file["attribute"]),
                CountLineComment=ifExist(
                    'CountLineComment', file["attribute"]),
                CountPath=ifExist('CountPath', file["attribute"]),
                CountStmt=ifExist('CountStmt', file["attribute"]),
                CountStmtDecl=ifExist('CountStmtDecl', file["attribute"]),
                CountStmtExe=ifExist('CountStmtExe', file["attribute"]),
                Cyclomatic=ifExist('Cyclomatic', file["attribute"]),
                Essential=ifExist('Essential', file["attribute"]),
                MaxNesting=ifExist('MaxNesting', file["attribute"]),
                RatioCommentToCode=ifExist(
                    'RatioCommentToCode', file["attribute"]),
            )
        else:
            metrics_dto = FileMetrics(
                space_key=space_key,
                file_name=file["filename"],
                CountDeclClass=ifExist('CountDeclClass', file["attribute"]),
                CountDeclExecutableUnit=ifExist(
                    'CountDeclExecutableUnit', file["attribute"]),
                CountLine=ifExist('CountLine', file["attribute"]),
                CountLineBlank=ifExist('CountLineBlank', file["attribute"]),
                CountLineCode=ifExist('CountLineCode', file["attribute"]),
                CountLineCodeDecl=ifExist(
                    'CountLineCodeDecl', file["attribute"]),
                CountDeclFunction=ifExist(
                    'CountDeclFunction', file["attribute"]),
                CountLineCodeExe=ifExist(
                    'CountLineCodeExe', file["attribute"]),
                CountLineComment=ifExist(
                    'CountLineComment', file["attribute"]),
                CountPath=ifExist('CountPath', file["attribute"]),
                CountStmt=ifExist('CountStmt', file["attribute"]),
                CountStmtDecl=ifExist('CountStmtDecl', file["attribute"]),
                CountStmtExe=ifExist('CountStmtExe', file["attribute"]),
                Cyclomatic=ifExist('Cyclomatic', file["attribute"]),
                Essential=ifExist('Essential', file["attribute"]),
                MaxNesting=ifExist('MaxNesting', file["attribute"]),
                RatioCommentToCode=ifExist(
                    'RatioCommentToCode', file["attribute"]),
                source=source
            )
            metrics_dto.save()

    metrics = metrics[0]
    if GitMetrics.objects.filter(space_key=space_key, source=source).exists():
        GitMetrics.objects.filter(space_key=space_key, source=source).update(
            CountDeclClass=ifExist('CountDeclClass', metrics),
            CountDeclExecutableUnit=ifExist(
                'CountDeclExecutableUnit', metrics),
            CountDeclFunction=ifExist('CountDeclFunction', metrics),
            CountDeclMethod=ifExist('CountDeclMethod', metrics),
            CountDeclMethodAll=ifExist('CountDeclMethodAll', metrics),
            CountLine=ifExist('CountLine', metrics),
            CountLineBlank=ifExist('CountLineBlank', metrics),
            CountLineCode=ifExist('CountLineCode', metrics),
            CountDeclFile=ifExist('CountDeclFile', metrics),
            CountLineCodeDecl=ifExist('CountLineCodeDecl', metrics),
            CountLineCodeExe=ifExist('CountLineCodeExe', metrics),
            CountLineComment=ifExist('CountLineComment', metrics),
            CountPath=ifExist('CountPath', metrics),
            CountStmt=ifExist('CountStmt', metrics),
            CountStmtDecl=ifExist('CountStmtDecl', metrics),
            CountStmtExe=ifExist('CountStmtExe', metrics),
            Cyclomatic=ifExist('Cyclomatic', metrics),
            Essential=ifExist('Essential', metrics),
            MaxNesting=ifExist('MaxNesting', metrics),
            RatioCommentToCode=ifExist('RatioCommentToCode', metrics),
        )
    else:
        metrics_dto = GitMetrics(
            space_key=space_key,
            CountDeclClass=ifExist('CountDeclClass', metrics),
            CountDeclExecutableUnit=ifExist(
                'CountDeclExecutableUnit', metrics),
            CountDeclFunction=ifExist('CountDeclFunction', metrics),
            CountDeclMethod=ifExist('CountDeclMethod', metrics),
            CountDeclMethodAll=ifExist('CountDeclMethodAll', metrics),
            CountLine=ifExist('CountLine', metrics),
            CountLineBlank=ifExist('CountLineBlank', metrics),
            CountLineCode=ifExist('CountLineCode', metrics),
            CountDeclFile=ifExist('CountDeclFile', metrics),
            CountLineCodeDecl=ifExist('CountLineCodeDecl', metrics),
            CountLineCodeExe=ifExist('CountLineCodeExe', metrics),
            CountLineComment=ifExist('CountLineComment', metrics),
            CountPath=ifExist('CountPath', metrics),
            CountStmt=ifExist('CountStmt', metrics),
            CountStmtDecl=ifExist('CountStmtDecl', metrics),
            CountStmtExe=ifExist('CountStmtExe', metrics),
            Cyclomatic=ifExist('Cyclomatic', metrics),
            Essential=ifExist('Essential', metrics),
            MaxNesting=ifExist('MaxNesting', metrics),
            RatioCommentToCode=ifExist('RatioCommentToCode', metrics),
            source=source
        )
        metrics_dto.save()


def ifExist(str, metric):
    if str in metric.keys():
        return metric[str]
    else:
        return 0


def takeCodeLine(dict):
    return dict.get("attribute").get("CountLineCode")


def sortTopTen(metrics):
    if len(metrics) < 10:
        return metrics
    else:
        metrics.sort(key=takeCodeLine, reverse=True)
        return metrics[0:10]


def auto_update_metrics():
    for relation in ProjectCoordinatorRelation.objects.all():
        get_metrics(relation)


utils.start_schedule(auto_update_commits, 60 * 60 * 24, None)
utils.start_schedule(update_individual_commits, 60 * 60 * 24)
utils.start_schedule(autoUpdateCommits, 60 * 60 * 24)
utils.start_schedule(auto_update_metrics, 60 * 60 * 24)
