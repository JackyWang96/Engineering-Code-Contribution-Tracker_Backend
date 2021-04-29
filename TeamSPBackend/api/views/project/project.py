from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import json

from TeamSPBackend.common.choices import RespCode
from TeamSPBackend.coordinator.models import Coordinator
from TeamSPBackend.project.models import ProjectCoordinatorRelation
from TeamSPBackend.common.utils import check_body, \
    body_extract, init_http_response
from TeamSPBackend.api.dto.dto import ProjectDTO
from TeamSPBackend.project.views import import_projects_into_coordinator


@require_http_methods(['POST'])
# @check_body
def import_project_in_batch(request, *args, **kwargs):
    # Method: POST
    try:
        query_dict = request.POST
        coordinator = query_dict['coordinator']
        project_list = [x.strip() for x in query_dict['project_list'].split(',')]
        # get coordinator_id based on coordinator_name
        if len(Coordinator.objects.filter(coordinator_name=coordinator)) == 0:
            print('No existing coordinator')
        else:
            coordinator_id = Coordinator.objects.filter(coordinator_name=coordinator)[0].id
            for x in project_list:
                import_project(coordinator_id, x)
        resp = init_http_response(
            RespCode.success.value.key, RespCode.success.value.msg)
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'code': -1, 'msg': 'error'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


def import_project(coordinator_id, project):
    # check if this relation has already existed to avoid overwrite
    if len(ProjectCoordinatorRelation.objects.filter(coordinator_id=coordinator_id, space_key=project)) == 0:
        relation = ProjectCoordinatorRelation(coordinator_id=coordinator_id,space_key=project)
        relation.save()
    pass