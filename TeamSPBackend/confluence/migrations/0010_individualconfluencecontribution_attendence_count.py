# Generated by Django 3.0.6 on 2021-10-14 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confluence', '0009_update_meetingminutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualconfluencecontribution',
            name='attendence_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
