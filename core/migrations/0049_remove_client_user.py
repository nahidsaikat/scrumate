# Generated by Django 2.1.7 on 2019-05-08 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_auto_20190508_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='user',
        ),
    ]