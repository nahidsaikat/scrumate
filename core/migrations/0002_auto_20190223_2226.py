# Generated by Django 2.1.7 on 2019-02-23 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='client_id',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='entry_date',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.IntegerField(default=None),
        ),
    ]
