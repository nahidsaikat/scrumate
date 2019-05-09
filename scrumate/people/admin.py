from django.contrib import admin
from scrumate.people.models import Department, Designation, Employee, Client


admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee)
admin.site.register(Client)
