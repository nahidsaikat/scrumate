# Generated by Django 2.1.7 on 2019-03-26 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20190326_1341'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliverable',
            options={'permissions': (('update_deliverable_status', 'Can Update Status of Deliverable'),)},
        ),
    ]
