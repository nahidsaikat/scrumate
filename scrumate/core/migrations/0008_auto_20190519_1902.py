# Generated by Django 2.2.1 on 2019-05-19 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190519_1147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('update_project_status', 'Can Update Status of Project'), ('view_commit_logs', 'Can View Commit Logs of Project'), ('project_status_report', 'Can See Project Status Report'), ('project_status_report_download', 'Can Download Project Status Report'), ('project_members', 'Can See Members of a Project'))},
        ),
    ]
