from djchoices import DjangoChoices, ChoiceItem


class TaskStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    InProgress = ChoiceItem(2, 'In Progress')
    PartiallyDone = ChoiceItem(3, 'Partially Done')
    Done = ChoiceItem(4, 'Done')
    Delivered = ChoiceItem(5, 'Delivered')
    NotDone = ChoiceItem(6, 'Not Done')
    Rejected = ChoiceItem(7, 'Rejected')


class Category(DjangoChoices):
    Analysis = ChoiceItem(1, 'Analysis')
    Development = ChoiceItem(2, 'Development')
    Testing = ChoiceItem(3, 'Testing')
    Implementation = ChoiceItem(4, 'Implementation')
