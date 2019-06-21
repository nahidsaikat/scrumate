from django.db import models
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords

from scrumate.general.choices import Column

User = get_user_model()


class Label(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')

    def __str__(self):
        return self.name


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    activity_text = models.TextField(default='')
    activity_data = models.TextField(default='')


class Dashboard(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("dev_dashboard", "Can See Dev Dashboard"),
        )


class Portlet(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    html_template = models.CharField(max_length=100)
    data_url = models.CharField(max_length=100)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class DashboardPortlet(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    portlet = models.ForeignKey(Portlet, on_delete=models.CASCADE)
    column = models.IntegerField(choices=Column, default=Column.One)
    height = models.DecimalField(default=50, decimal_places=2, max_digits=15)
    width = models.DecimalField(default=100, decimal_places=2, max_digits=15)

    history = HistoricalRecords()
