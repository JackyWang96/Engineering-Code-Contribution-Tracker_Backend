# Generated by Django 3.0.6 on 2021-10-11 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confluence', '0008_userlist_jira_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingminutes',
            name='end_time',
            field=models.CharField(default=0, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetingminutes',
            name='meeting_type',
            field=models.CharField(default=0, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetingminutes',
            name='start_time',
            field=models.CharField(default=0, max_length=256),
            preserve_default=False,
        ),
    ]