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
