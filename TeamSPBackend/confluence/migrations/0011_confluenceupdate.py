# Generated by Django 3.1.13 on 2021-10-17 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confluence', '0010_individualconfluencecontribution_attendence_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfluenceUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('displayName', models.CharField(max_length=256)),
                ('time', models.CharField(max_length=512)),
                ('url', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'confluence_update_information',
            },
        ),
    ]
