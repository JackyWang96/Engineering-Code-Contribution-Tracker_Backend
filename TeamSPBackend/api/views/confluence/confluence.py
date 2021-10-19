from atlassian import Confluence
import json
import requests
from requests.auth import HTTPBasicAuth
from TeamSPBackend.confluence.models import PageHistory, UserList, IndividualConfluenceContribution, MeetingMinutes, ConfluenceUpdate
from TeamSPBackend.common.choices import RespCode
from django.views.decorators.http import require_http_methods
from django.http.response import HttpResponse
from TeamSPBackend.common.github_util import convert
from TeamSPBackend.common.utils import init_http_response, check_login, make_json_response, init_http_response_my_enum
from TeamSPBackend.confluence.models import UserList
from TeamSPBackend.confluence.models import MeetingMinutes

from TeamSPBackend.project.models import ProjectCoordinatorRelation

from TeamSPBackend.confluence.models import PageHistory
from TeamSPBackend.coordinator.models import Coordinator
from TeamSPBackend.api import config
from atlassian import Confluence
from datetime import datetime

from atlassian import Confluence
from datetime import datetime


def getIformation(request):
    try:
        username = config.atl_username
        password = config.atl_password
        confluence = log_into_confluence(username, password)

        resp = confluence
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
def getAllspace(request):

    try:

        username = config.atl_username
        password = config.atl_password
        confluence = log_into_confluence(username, password)

        meetingNotes = confluence.get_all_spaces(
            start=0, limit=10, expand=None)
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = meetingNotes

        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
def getTest(request):

    try:
        username = config.atl_username
        password = config.atl_password
        confluence = log_into_confluence(username, password)

  
        convert = confluence.get_page_by_id(page_id='78333963')
        
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        list=[]
        # for version in convert:
        #     data = {
        #     "username": convert.get("lastUpdated").get("by").get("username"),
        #     "displayName": convert.get("lastUpdated").get("by").get("displayName"),
        #     "createdDate": convert.get("lastUpdated").get("when"),
        #     "url": convert.get("lastUpdated").get("_links").get("self"),
    
        #     }

        # list.append(data)
        # for page in convert:
        #     data.append({
        #         'id': page['id'],
        #         'type': page['type'],
        #         'title': page['title']
        #     })
       

        resp['data'] = convert
        

        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


def getUpdate(contentId):

    try:
        
        username = config.atl_username
        password = config.atl_password
        confluence = log_into_confluence(username, password)
        convert = confluence.get_attachment_history(attachment_id=contentId)
        

        
        
        
        
        list=[]
        for known in convert:
            
            list.append ({
            "title": confluence.get_page_by_id(contentId)['title'],
            "displayName": known["by"]["displayName"],
            "Time": known["when"],
            "url": 'https://confluence.cis.unimelb.edu.au:8443'+confluence.get_page_by_id(contentId)['space']["_links"]["webui"]+'/'+confluence.get_page_by_id(contentId)['title']
            
            })

        # resp['data'] = convert
        return list

    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['POST'])
def update_git_username(request):
    """Get users github username
    Method: post
    """
    json_body = json.loads(request.body)
    id = json_body.get("user_id")
    git_username = json_body.get("git_username")
    try:
        user = UserList.objects.get(user_id=id)
        user.git_username = git_username
        user.save()
        resp = init_http_response_my_enum(RespCode.success)
        return make_json_response(resp=resp)
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['POST'])
def update_jira_username(request):
    """Get users github username
    Method: post
    """
    json_body = json.loads(request.body)
    id = json_body.get("user_id")
    jira_username = json_body.get("jira_username")
    try:
        user = UserList.objects.get(user_id=id)
        user.jira_username = jira_username
        user.save()
        resp = init_http_response_my_enum(RespCode.success)
        return make_json_response(resp=resp)
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
def get_all_groups(request):
    """Get all groups accessable by the logged in user
    Method: GET
    """
    user = request.session.get('user')
    username = user['atl_username']
    password = user['atl_password']

    try:
        confluence = log_into_confluence(username, password)
        conf_resp = confluence.get_all_groups()

        data = []
        for group in conf_resp:

            print(group)
            data.append({
                'type': group['type'],
                'name': group['name']
            })
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
def get_space(request, space_key):
    """Get a Confluence Space
    Method: GET
    Request: space_key
    """
    user = request.session.get('user')
    username = user['atl_username']
    password = user['atl_password']
    try:
        confluence = log_into_confluence(username, password)
        conf_resp = confluence.get_space(
            space_key, expand='homepage')
        conf_homepage = conf_resp['homepage']
        data = {
            'id': conf_resp['id'],
            'key': conf_resp['key'],
            'name': conf_resp['name'],
            'homepage': {
                'id': conf_homepage['id'],
                'type': conf_homepage['type'],
                'title': conf_homepage['title'],

            }
        }
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
def get_pages_of_space(request, space_key):
    """Get all the pages under the Confluence Space
    Method: GET
    Request: space
    """
    user = request.session.get('user')
    username = user['atl_username']
    password = user['atl_password']

    try:
        confluence = log_into_confluence(username, password)
        conf_resp = confluence.get_all_pages_from_space(space_key)
        data = []
        for page in conf_resp:
            data.append({
                'id': page['id'],
                'type': page['type'],
                'title': page['title']
            })
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    # Get Page Content by ID (HTML) (lower prio for now)


def get_all_pages_of_space(space_key):
    """Get all the pages under the Confluence Space
    Method: GET
    Request: space
    """

    username = config.atl_username
    password = config.atl_password

    # try:
    confluence = log_into_confluence(username, password)
    conf_resp = confluence.get_all_pages_from_space(space_key)
    data = []
    for page in conf_resp:
        data.append(page['id'])

    # resp['data'] = data
    return data


@require_http_methods(['GET'])
def get_all_update(request, space_key):
    """Get all the pages under the Confluence Space
    Method: GET
    Request: space
    """
    user = request.session.get('user')
    # username = user['atl_username']
    # password = user['atl_password']

    username = config.atl_username
    password = config.atl_password
    try:
        confluence = log_into_confluence(username, password)

        convert = get_all_pages_of_space(space_key)

        for id in convert:
            data = (getUpdate(contentId=id))
            for item in data:
                update = ConfluenceUpdate.objects.create(
                    title=item.get("title"),
                    displayName=item.get("displayName"),
                    time=item.get("Time"),
                    url=item.get("url")

                )

                update.save()

        # resp = init_http_response(
        #     RespCode.success.value.key, RespCode.success.value.msg)

        return HttpResponse(json.dumps(data), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
def search_team(request, keyword):
    user = request.session.get('user')
    username = user['atl_username']
    password = user['atl_password']
    try:
        confluence = log_into_confluence(username, password)
        conf_resp = confluence.get_all_groups()
        data = []
        result = []
        for group in conf_resp:
            data.append({
                'type': group['type'],
                'name': group['name']
            })
        for element in data:
            if keyword.lower() in element['name'].lower():
                result.append({
                    'name': element['name']
                })
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = result
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
def get_group_members(request, group):
    """Get all the members under 'group_name' of the Confluence Space
    Method: GET
    Request: group_name
    """
    try:
        user = request.session.get('user')
        username = user['atl_username']
        password = user['atl_password']
        group_name = group
        confluence = log_into_confluence(username, password)
        conf_resp = confluence.get_group_members(group_name)
        data = []
        for user in conf_resp:
            data.append({
                # 'type': user['type'],
                # 'userKey': user['userKey'],
                # 'profilePicture': user['profilePicture'],
                'name': user['displayName'],
                'email': user['username'] + "@student.unimelb.edu.au"
            })
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
def get_user_details(request, member):
    """Get a specific Confluence Space member's details
    Method: POST
    Request: member's username
    """

    user = request.session.get('user')
    username = user['atl_username']
    password = user['atl_password']
    try:
        confluence = log_into_confluence(username, password)
        conf_resp = confluence.get_user_details_by_username(member)
        data = {
            'type': conf_resp['type'],
            'username': conf_resp['username'],
            'userKey': conf_resp['userKey'],
            'profilePicture': conf_resp['profilePicture'],
            'displayName': conf_resp['displayName']
        }
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
def get_subject_supervisors(request, subjectcode, year):
    user = request.session.get('user')
    username = user['atl_username']
    password = user['atl_password']
    try:
        confluence = log_into_confluence(username, password)
        conf_resp = confluence.get_all_groups()
        supervisors = []
        data = []
        for group in conf_resp:
            if "staff" in group['name'] and year in group['name'] and subjectcode in group['name']:
                supervisors = confluence.get_group_members(group['name'])

        for each in supervisors:
            data.append({
                # 'type': user['type'],
                # 'userKey': user['userKey'],
                # 'profilePicture': user['profilePicture'],
                'name': each['displayName'],
                'email': each['username']
            })
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
def get_page_contributors(request, *args, **kwargs):
    """Get a Confluence page's contributors
    Method: Get
    Request: page_id
    """
    user = request.session.get('user')
    username = user['atl_username']
    password = user['atl_password']

    try:
        confluence = log_into_confluence(username, password)
        page_id = kwargs['page_id']
        # page_id = kwargs['page_id']

        # Todo: change these to configurable inputs
        domain = "https://confluence.cis.unimelb.edu.au"
        port = "8443"
        url = f"{domain}:{port}/rest/api/content/{page_id}/history?expand=contributors.publishers.users"

        # parameters = {"expand": "contributors.publishers.users"}
        conf_resp = requests.get(
            url=url, auth=HTTPBasicAuth(username, password))

        # url=url, params=parameters, auth=HTTPBasicAuth(username, password)).json()
        convert = json.loads(conf_resp)
        data = {
            "createdBy": conf_resp["createdBy"],
            "createdDate": conf_resp["createdDate"],
            "contributors": conf_resp["contributors"]
        }
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}

        return HttpResponse(json.dumps(resp), content_type="application/json")


def log_into_confluence(username, password):
    confluence = Confluence(
        url='https://confluence.cis.unimelb.edu.au:8443/',
        username=username,
        password=password,

        verify_ssl=False
    )
    return confluence


def get_members(request, group):
    try:
        user = request.session.get('user')
        username = user['atl_username']
        password = user['atl_password']
        confluence = log_into_confluence(username, password)
        conf_resp = confluence.get_group_members(group)
        data = []
        for user in conf_resp:
            data.append({
                # 'type': user['type'],
                # 'userKey': user['userKey'],
                # 'profilePicture': user['profilePicture'],
                'name': user['displayName'],
                'email': user['username'] + "@student.unimelb.edu.au"
            })
        return data
    except Exception as e:
        print(e)
        return None


@require_http_methods(['GET'])
@check_login()
def get_spaces_by_key(request, key_word):
    """Get a list of Confluence space keys that contains the key word
    Method: GET
    Request: key_word
    """
    username = config.atl_username
    password = config.atl_password
    try:
        confluence = log_into_confluence(username, password)
        spaces = confluence.get_all_spaces()
        space_keys = [space['key']
                      for space in spaces if key_word.lower() in space['key'].lower()]
        while len(spaces) > 0:
            spaces = confluence.get_all_spaces(start=len(spaces))
            space_keys.extend(
                [space['key'] for space in spaces if key_word.lower() in space['key'].lower()])

        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = space_keys
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
@check_login()
def get_user_list(request, space_key):
    """Get the user list in a Confluence space
    Method: Get
    Parameter: space_key
    """
    try:
        user_list = []
        for user_info in UserList.objects.filter(space_key=space_key):
            user_detail = {
                "name": user_info.user_name,
                "id": user_info.user_id,
                "email": user_info.email,
                "picture": user_info.picture,
                "git_name": user_info.git_username,
                "jira_name": user_info.jira_username
            }
            user_list.append(user_detail)
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = {"total": len(user_list),
                        "user_list": user_list}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
@check_login()
def get_meeting_minutes(request, space_key):
    """
        return all the meeting minutes titles and links from the specific confluence space
        step1: get the space_key
        step2: find all the minutes which have the same space key
        step3: return the titles and links
    """
    # user = request.session.get('user')
    # username = user['atl_username']
    # password = user['atl_password']
    key = space_key
    try:
        # find all the meeting minutes which have the specific space key
        meeting_minutes = MeetingMinutes.objects.filter(space_key=key)
        data = []
        for meeting in meeting_minutes:
            data.append({
                'title': meeting.meeting_title,
                'start': meeting.start_time,
                'end': meeting.end_time,
                'type': meeting.meeting_type,
                'link': meeting.meeting_link
            })
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
@check_login()
def get_page_count_by_time(request, space_key):
    """Get a list of time, page count pairs.
    From this space is created, to the date this method is called, one a daily basis.
    Method: GET
    Request: space_key
    """
    try:
        data = []
        for page_history in PageHistory.objects.filter(space_key=space_key):
            history = {
                "time": page_history.date,
                "page_count": page_history.page_count
            }
            data.append(history)

        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['GET'])
@check_login()
def get_imported_project(request):
    """
    get the imported projects
    Method: GET
    Request: coordinator_id
    Return: status code, message, list of project space keys and space names
    """
    # user = request.session.get('user')
    # username = user['atl_username']
    # password = user['atl_password']
    username = config.atl_username
    password = config.atl_password
    coordinator_id = request.session.get('coordinator_id')

    try:
        confluence = log_into_confluence(username, password)
        data = []
        # get all the space keys from DB where coordinator_id = given id
        for project in ProjectCoordinatorRelation.objects.filter(coordinator_id=coordinator_id):
            space_key = project.space_key
            space = confluence.get_space(space_key)
            space_name = space['name']
            data.append({
                'space_key': space_key,
                'space_name': space_name
            })
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(['POST'])
@check_login()
def delete_project(request, *args, **kwargs):
    try:
        # delete space key that is imported by the coordinator.
        space_key = json.loads(request.body)["space_key"]
        coordinator_id = request.session['coordinator_id']
        ProjectCoordinatorRelation.objects.filter(
            coordinator_id=coordinator_id, space_key=space_key).delete()
        resp = {'code': RespCode.success.value.key,
                'msg': RespCode.success.value.msg}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


def get_Confluence_Newst(request, url, *args, **kwargs):
    
    information = ConfluenceUpdate.objects.filter(url__contains=url).exclude(displayName__in=['Ankita Dhar','Akil Munusamy Pitchandi','Sharodh Keelamanakudi Ragupathi','admin admin','Pawan Malhotra','Abdul Rehman Mohammad','YALAN ZHAO'])
    list=[]
    for x in information:
        dict = {
            "title": x.title,
            'displayName': x.displayName,

            'url': x.url

        }
        list.append(dict)
    return HttpResponse(json.dumps(list), content_type="application/json")


def get_confluence_update_information(request, url, *args, **kwargs):

    information = ConfluenceUpdate.objects.filter(url__contains=url).exclude(displayName__in=[
        'Ankita Dhar', 'Akil Munusamy Pitchandi', 'Sharodh Keelamanakudi Ragupathi', 'admin admin', 'Pawan Malhotra', 'Abdul Rehman Mohammad', 'YALAN ZHAO'])

    list = []
    for x in information:
        dict = {
            "title": x.title,
            'displayName': x.displayName,
            'time': x.time,
            'url': x.url

        }
        list.append(dict)
    return HttpResponse(json.dumps(list), content_type="application/json")

def get_all_version_content_history_by_url(self, url):
        """
        Get content history by version number
        :param content_id:
        :param version_number:
        :return:
        """
        x=url.split('https://confluence.cis.unimelb.edu.au:8443/')
        
        print(x[1])
        return self.get(x[1])

def get_all_version_content_history_by_page_id(self, content_id):
        """
        Get content history by version number
        :param content_id:
        :param version_number:
        :return:
        """
        url = 'rest/experimental/content/{0}/version/'.format(content_id)
       
        
        return self.get(url).get('results')





        

