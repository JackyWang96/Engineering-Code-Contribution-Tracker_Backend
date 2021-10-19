# Generated by Django 3.0.6 on 2021-10-14 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0011_gitcontribution_space_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitLastCommit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=256)),
                ('username', models.CharField(max_length=256)),
                ('date', models.CharField(max_length=256)),
                ('message', models.CharField(max_length=512)),
                ('space_key', models.CharField(max_length=256)),
                ('source', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'git_last_commit',
            },
        ),
        migrations.RenameField(
            model_name='gitcontribution',
            old_name='author',
            new_name='git_username',
        ),
        migrations.AddField(
            model_name='gitcontribution',
            name='username',
            field=models.CharField(default=0, max_length=256),
            preserve_default=False,
        ),
    ]
