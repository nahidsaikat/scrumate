# Generated by Django 2.1.7 on 2019-05-08 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20190508_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyscrum',
            name='issue',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Issue'),
        ),
        migrations.AlterField(
            model_name='dailyscrum',
            name='project',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Project'),
        ),
        migrations.AlterField(
            model_name='dailyscrum',
            name='release',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Release'),
        ),
        migrations.AlterField(
            model_name='dailyscrum',
            name='task',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Task'),
        ),
        migrations.AlterField(
            model_name='dailyscrum',
            name='user_story',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.UserStory'),
        ),
    ]
