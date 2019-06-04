from djchoices import DjangoChoices, ChoiceItem


class ProjectMemberRole(DjangoChoices):
    ProjectOwner = ChoiceItem(1, 'ProjectOwner')
    TeamLead = ChoiceItem(2, 'TeamLead')
    Developer = ChoiceItem(3, 'Developer')
