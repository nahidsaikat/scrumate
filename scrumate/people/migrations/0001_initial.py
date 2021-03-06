# Generated by Django 2.2.1 on 2019-05-09 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=50)),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.IntegerField(blank=True, choices=[(1, 'Mr.'), (2, 'Mrs.'), (3, 'Miss')], default=1, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('full_name', models.CharField(blank=True, max_length=200)),
                ('nick_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('address_line_1', models.CharField(max_length=100, null=True)),
                ('address_line_2', models.CharField(blank=True, max_length=100, null=True)),
                ('address_line_3', models.CharField(blank=True, max_length=100, null=True)),
                ('address_line_4', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('party_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='people.Party')),
                ('type', models.IntegerField(choices=[(1, 'Employee'), (2, 'Customer'), (3, 'Vendor')], default=2)),
                ('sub_type', models.IntegerField(choices=[(1, 'Individual'), (2, 'Organization')], default=2)),
            ],
            bases=('people.party',),
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('rank', models.IntegerField(blank=True, default=None, null=True)),
                ('department', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='people.Department')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.Designation')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('party_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='people.Party')),
                ('type', models.IntegerField(choices=[(1, 'Employee'), (2, 'Customer'), (3, 'Vendor')], default=1)),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female')], default=1)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('department', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.Department')),
                ('designation', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.Designation')),
                ('user', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('people.party',),
        ),
    ]
