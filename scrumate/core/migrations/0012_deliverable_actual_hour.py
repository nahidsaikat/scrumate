# Generated by Django 2.2.1 on 2019-06-02 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190531_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverable',
            name='actual_hour',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True, verbose_name='Point'),
        ),
    ]
