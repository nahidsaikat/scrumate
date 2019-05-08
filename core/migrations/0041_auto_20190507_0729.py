# Generated by Django 2.1.7 on 2019-05-07 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20190507_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='approved_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_releases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='release',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_releases', to=settings.AUTH_USER_MODEL),
        ),
    ]