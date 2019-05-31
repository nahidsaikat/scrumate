# Generated by Django 2.2.1 on 2019-05-31 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190531_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectcommitlog',
            old_name='author_html_url',
            new_name='html_url',
        ),
        migrations.RenameField(
            model_name='projectcommitlog',
            old_name='author_url',
            new_name='url',
        ),
        migrations.AlterField(
            model_name='projectcommitlog',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commit_log', to='core.Project'),
        ),
        migrations.AlterField(
            model_name='projectcommitlog',
            name='sha',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
