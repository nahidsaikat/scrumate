from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from scrumate.people.models import Department, Designation, Employee, Client


admin.site.register(Department, SimpleHistoryAdmin)
admin.site.register(Designation, SimpleHistoryAdmin)
admin.site.register(Employee, SimpleHistoryAdmin)
admin.site.register(Client, SimpleHistoryAdmin)
