# Generated by Django 2.2.2 on 2019-06-22 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_auto_20190622_1941'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'permissions': (('department_history', 'Can See Department History'),)},
        ),
        migrations.AlterModelOptions(
            name='designation',
            options={'permissions': (('designation_history', 'Can See Designation History'),)},
        ),
    ]