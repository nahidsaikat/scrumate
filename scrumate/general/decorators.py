from django.core.exceptions import PermissionDenied
from scrumate.core.member.choices import ProjectMemberRole


def admin_user(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def project_owner(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        project_member = request.user.employee.projectmember_set.first()
        if project_member and project_member.role == ProjectMemberRole.ProjectOwner:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def team_lead(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        project_member = request.user.employee.projectmember_set.first()
        if project_member and project_member.role == ProjectMemberRole.TeamLead:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def developer(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        project_member = request.user.employee.projectmember_set.first()
        if project_member and project_member.role == ProjectMemberRole.Developer:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def owner_or_lead(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        project_member = request.user.employee.projectmember_set.first()
        if project_member and project_member.role in [ProjectMemberRole.ProjectOwner, ProjectMemberRole.TeamLead]:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
