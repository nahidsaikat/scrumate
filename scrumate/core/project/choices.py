from djchoices import DjangoChoices, ChoiceItem


class ProjectStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    InProgress = ChoiceItem(2, 'In Progress')
    Completed = ChoiceItem(3, 'Completed')


class ProjectType(DjangoChoices):
    Public = ChoiceItem(1, 'Public')
    Private = ChoiceItem(2, 'Private')
    InHouse = ChoiceItem(3, 'In House')
