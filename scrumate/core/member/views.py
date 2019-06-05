from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from scrumate.general.decorators import project_owner
from scrumate.core.project.models import Project
from scrumate.core.member.models import ProjectMember
from scrumate.core.member.forms import ProjectMemberForm


@login_required(login_url='/login/')
@permission_required('core.project_members', raise_exception=True)
def project_member_list(request, project_id, **kwargs):
    project = Project.objects.get(pk=project_id)

    member_list = project.projectmember_set.all()

    return render(request, 'core/projects/project_member_list.html', {
        'member_list': member_list,
        'project': project
    })


@project_owner
@login_required(login_url='/login/')
@permission_required('core.project_members', raise_exception=True)
def project_member_add(request, project_id, **kwargs):
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        form = ProjectMemberForm(request.POST)
        user_id = request.POST.get('user')
        already_assigned = ProjectMember.objects.filter(project_id=project_id, user_id=user_id).count()
        if already_assigned:
            form.add_error('user', 'User is already in the team!')
        elif form.is_valid():
            member = form.save(commit=False)
            member.project = project
            member.save()
            return redirect('project_member_list', permanent=True, project_id=project_id)
    else:
        form = ProjectMemberForm()

    title = 'Add Member'
    return render(request, 'core/common_add.html', {'form': form, 'title': title,
                                                    'list_url_name': 'project_member_list', 'project': project})


@project_owner
@login_required(login_url='/login/')
@permission_required('core.project_members', raise_exception=True)
def project_member_edit(request, project_id, pk, **kwargs):
    instance = get_object_or_404(ProjectMember, id=pk)
    form = ProjectMemberForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('project_member_list', permanent=True, project_id=project_id)

    title = 'Edit Member'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title,
                                                    'list_url_name': 'project_member_list', 'project': project})


@project_owner
@login_required(login_url='/login/')
@permission_required('core.project_members', raise_exception=True)
def project_member_delete(request, project_id, pk, **kwargs):
    instance = get_object_or_404(ProjectMember, id=pk)
    if instance:
        instance.delete()
        return redirect('project_member_list', permanent=True, project_id=project_id)

    title = 'Delete Member'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'title': title,
                                                    'list_url_name': 'project_member_list', 'project': project})
