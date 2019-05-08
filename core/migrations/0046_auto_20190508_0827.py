# Generated by Django 2.1.7 on 2019-05-08 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_auto_20190508_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='designation',
            name='department',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Department'),
        ),
        migrations.AlterField(
            model_name='designation',
            name='rank',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
