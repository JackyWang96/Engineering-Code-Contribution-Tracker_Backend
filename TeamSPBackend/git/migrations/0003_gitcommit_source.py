# Generated by Django 3.0.6 on 2021-09-28 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0002_auto_20210928_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitcommit',
            name='source',
            field=models.CharField(default=0, max_length=256),
            preserve_default=False,
        ),
    ]