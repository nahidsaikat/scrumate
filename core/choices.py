from django.utils.translation import gettext as _
from djchoices import DjangoChoices, ChoiceItem


class ProjectStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    InProgress = ChoiceItem(2, 'In Progress')
    Completed = ChoiceItem(3, 'Completed')

PROJECT_TYPE_CHOICES = (
    (1, _("Public")),
    (2, _("Private")),
    (3, _("In House")),
)

PRIORITY_CHOICES = (
    (1, _("Low")),
    (2, _("Medium")),
    (3, _("High")),
)

USERSTORY_STATUS_CHOICES = (
    (1, _("Pending")),
    (2, _("Analysing")),
    (3, _("Analysis Complete")),
    (4, _("Developing")),
    (5, _("Development Complete")),
    (6, _("Delivered")),
)

SPRINT_STATUS_CHOICES = (
    (1, _("Pending")),
    (2, _("On Going")),
    (3, _("Completed")),
)

COLUMN_CHOICES = (
    (1, _("One")),
    (2, _("Two")),
    (3, _("Three")),
)

CATEGORY_CHOICES = (
    (1, _("Analysis")),
    (2, _("Development")),
    (3, _("Testing")),
    (4, _("Implementation")),
)

TASK_STATUS_CHOICES = (
    (1, _("Pending")),
    (2, _("In Progress")),
    (3, _("Partially Done")),
    (4, _("Done")),
    (5, _("Delivered")),
    (6, _("Not Done")),
    (7, _("Rejected")),
)

DELIVERABLE_STATUS_CHOICES = (
    (1, _("Pending")),
    (2, _("In Progress")),
    (3, _("Partially Done")),
    (4, _("Done")),
    (5, _("Delivered")),
    (6, _("Not Done")),
    (7, _("Rejected")),
)

class DeliverableStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    InProgress = ChoiceItem(2, 'In Progress')
    PartiallyDone = ChoiceItem(3, 'Partially Done')
    Done = ChoiceItem(4, 'Done')
    Delivered = ChoiceItem(5, 'Delivered')
    NotDone = ChoiceItem(6, 'Not Done')
    Rejected = ChoiceItem(7, 'Rejected')

OVER_TIME_STTUS_CHOICES = (
    (1, _("Pending")),
    (2, _("Acknowledged")),
    (3, _("Done")),
    (4, _("Rejected")),
)

PARTY_TYPE_CHOICES = (
    (1, _("Employee")),
    (2, _("Customer")),
    (3, _("Vendor")),
)

PARTY_SUBTYPE_CHOICES = (
    (1, _("Individual")),
    (2, _("Organization")),
)

PARTY_GENDER_CHOICES = (
    (1, _("Male")),
    (2, _("Female")),
)

PARTY_TITLE_CHOICES = (
    (1, _("Mr.")),
    (2, _("Mrs.")),
    (3, _("Miss")),
)
