# Generated by Django 2.1.7 on 2019-03-19 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20190319_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverable',
            name='assign_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='assignee',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Employee'),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='estimated_hour',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='priority',
            field=models.IntegerField(blank=True, choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=3, null=True),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='release_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'Pending'), (2, 'In Progress'), (3, 'Partially Done'), (4, 'Done'), (5, 'Delivered'), (6, 'Not Done'), (7, 'Rejected')], default=1, null=True),
        ),
    ]
