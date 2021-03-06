from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView

from scrumate.general.decorators import owner_or_lead
from scrumate.core.user_story.filters import UserStoryFilter
from scrumate.core.project.models import Project
from scrumate.core.user_story.models import UserStory
from scrumate.core.user_story.forms import UserStoryForm
from scrumate.general.views import HistoryList


@login_required(login_url='/login/')
def user_story_list(request, project_id, **kwargs):
    user_story_filter = UserStoryFilter(request.GET, queryset=UserStory.objects.filter(project_id=project_id).order_by('-id'))
    user_story_list = user_story_filter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(user_story_list, settings.PAGE_SIZE)
    try:
        user_stories = paginator.page(page)
    except PageNotAnInteger:
        user_stories = paginator.page(1)
    except EmptyPage:
        user_stories = paginator.page(paginator.num_pages)

    project = Project.objects.get(pk=project_id)
    return render(request, 'core/user_story_list.html', {'user_stories': user_stories, 'filter': user_story_filter, 'project': project})


@owner_or_lead
@login_required(login_url='/login/')
def user_story_add(request, project_id, **kwargs):
    if request.method == 'POST':
        form = UserStoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.analysed_by = getattr(request.user, 'employee', None)
            story.project_id = project_id
            story.save()
            messages.success(request, "User story added successfully!")
            return redirect('user_story_list', permanent=True, project_id=project_id)
        else:
            messages.error(request, "Invalid data!")
    else:
        form = UserStoryForm()

    title = 'New User Story'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title, 'list_url_name': 'user_story_list', 'project': project})

@owner_or_lead
@login_required(login_url='/login/')
def user_story_edit(request, project_id, pk, **kwargs):
    instance = get_object_or_404(UserStory, id=pk)
    form = UserStoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "User story updated successfully!")
        return redirect('user_story_list', project_id=project_id)
    else:
        messages.error(request, "Invalid data!")

    title = 'Edit User Story'
    project = Project.objects.get(pk=project_id)
    return render(request, 'core/common_add.html', {'form': form, 'title': title, 'list_url_name': 'user_story_list', 'project': project})


@owner_or_lead
@login_required(login_url='/login/')
@permission_required('core.update_user_story_status', raise_exception=True)
def update_user_story_status(request, project_id, pk, **kwargs):
    instance = get_object_or_404(UserStory, id=pk)
    form = UserStoryForm(request.POST or None, instance=instance)
    if request.POST:
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        messages.success(request, "User story status updated successfully!")
        return redirect('user_story_list', project_id=project_id)

    project = Project.objects.get(pk=project_id)
    return render(request, 'includes/single_field.html', {
        'field': form.visible_fields()[5],
        'title': 'Update Status',
        'url': reverse('user_story_list', kwargs={'project_id': project_id}),
        'project': project,
        'base_template': 'general/index_project_view.html'
    })


class UserStoryHistoryList(HistoryList):
    permission_required = 'scrumate.core.user_story_history'

    def get_user_story_id(self):
        return self.kwargs.get('pk')

    def get_project_id(self):
        return self.kwargs.get('project_id')

    def get_queryset(self):
        return UserStory.history.filter(id=self.get_user_story_id())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.get_project_id())
        user_story = UserStory.objects.get(pk=self.get_user_story_id())

        context['project'] = project
        context['title'] = f'History of {user_story.summary}'
        context['back_url'] = reverse('user_story_list', kwargs={'project_id': self.get_project_id()})
        context['base_template'] = 'general/index_project_view.html'
        return context


class UserStoryDetailView(DetailView):
    queryset = UserStory.objects.all()
    template_name = 'includes/generic_view.html'
    context_object_name = 'user_story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        instance = self.get_object()
        context['form'] = UserStoryForm(instance=instance)
        context['edit_url'] = reverse('user_story_edit', kwargs={'project_id': project_id, 'pk': instance.pk})
        context['list_url'] = reverse('user_story_list', kwargs={'project_id': project_id})
        context['title'] = instance.summary
        context['project'] = Project.objects.get(pk=project_id)
        context['base_template'] = 'general/index_project_view.html'
        return context
