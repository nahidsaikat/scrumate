from django.utils.translation import gettext as _

PROJECT_STATUS_CHOICES = (
    (1, _("Pending")),
    (2, _("In Progress")),
    (3, _("Completed")),
)

PROJECT_TYPE_CHOICES = (
    (1, _("Public")),
    (2, _("Private")),
    (3, _("In House")),
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

TASK_CHOICES = (
    (1, _("Pending")),
    (2, _("In Progress")),
    (3, _("Partially Done")),
    (4, _("Done")),
    (5, _("Delivered")),
    (6, _("Not Done")),
    (7, _("Rejected")),
)
