from django.db import models


# Create your models here.

class MeetingMinutes(models.Model):
    space_key = models.CharField(max_length=256, null=False)
    meeting_title = models.CharField(max_length=256, null=False)
    start_time = models.CharField(max_length=256, null=False)
    end_time = models.CharField(max_length=256, null=False)
    meeting_type = models.CharField(max_length=256, null=False)
    meeting_link = models.TextField(null=False)

    class Meta:
        db_table = 'meeting_minutes'


class UserList(models.Model):

    user_id = models.CharField(max_length=256, null=False)
    user_name = models.CharField(max_length=256, null=False)
    email = models.EmailField(max_length=256, null=False)
    picture = models.CharField(max_length=256, null=False)
    space_key = models.CharField(max_length=256, null=False)
    git_username = models.CharField(max_length=256, null=False)
    jira_username = models.CharField(max_length=256, null=False)

    class Meta:
        db_table = 'user_list'


class PageHistory(models.Model):
    page_count = models.IntegerField()
    date = models.IntegerField()
    space_key = models.CharField(max_length=256)

    class Meta:
        db_table = 'page_history'


class IndividualConfluenceContribution(models.Model):
    space_key = models.CharField(max_length=256)
    user_id = models.CharField(max_length=256)
    user_name = models.CharField(max_length=256)
    page_count = models.IntegerField()
    attendence_count = models.IntegerField()

    class Meta:
        db_table = 'individual_confluence_contribution'

class ConfluenceUpdate(models.Model):
    title = models.CharField(max_length=256, null=False)
    displayName = models.CharField(max_length=256, null=False)
    time = models.CharField(max_length=512, null=False)
    url = models.CharField(max_length=512, null=False)
    

    class Meta:
        db_table = 'confluence_update_information'


class ConfluenceNewUpdate(models.Model):
    title = models.CharField(max_length=256, null=False)
    displayName = models.CharField(max_length=256, null=False)
    url = models.CharField(max_length=512, null=False)
    

    class Meta:
        db_table = 'confluence_newest_page'