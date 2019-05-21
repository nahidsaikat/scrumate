from django.core.exceptions import PermissionDenied
from scrumate.core.models import Project


def role_wise_permission(function):
    def wrap(request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['project_id'])
        if request.user in project.projectmember_set.all():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_user(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_stuff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
