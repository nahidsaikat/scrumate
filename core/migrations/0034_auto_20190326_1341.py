# Generated by Django 2.1.7 on 2019-03-26 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20190326_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='day_wise_label',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='department',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Department'),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='end_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='start_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'Pending'), (2, 'On Going'), (3, 'Completed')], default=1, null=True),
        ),
    ]