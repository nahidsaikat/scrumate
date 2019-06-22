from django.db import models
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords
from simple_history import register

from scrumate.people.choices import PartyType, PartyGender, PartyTitle, PartySubType

User = get_user_model()
register(User, app=__package__)


class Division(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(default='')

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    # division = models.ForeignKey(Division, on_delete=models.SET_NULL, default=None, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, default=None, null=True)
    rank = models.IntegerField(default=None, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Party(models.Model):
    title = models.IntegerField(choices=PartyTitle.choices, default=PartyTitle.Mr, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=200, blank=True)
    nick_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    address_line_1 = models.CharField(max_length=100, null=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    address_line_3 = models.CharField(max_length=100, null=True, blank=True)
    address_line_4 = models.CharField(max_length=100, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.full_name


class Employee(Party):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='employee')
    type = models.IntegerField(choices=PartyType.choices, default=PartyType.Employee)
    gender = models.IntegerField(choices=PartyGender.choices, default=PartyGender.Male)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, default=None, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, default=None, null=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        permissions = (
            ("employee_history", "Can See Employee History"),
        )


class Client(Party):
    type = models.IntegerField(choices=PartyType.choices, default=PartyType.Customer)
    sub_type = models.IntegerField(choices=PartySubType.choices, default=PartySubType.Organization)

    class Meta:
        permissions = (
            ("client_history", "Can See Client History"),
        )

