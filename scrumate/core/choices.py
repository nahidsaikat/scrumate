from djchoices import DjangoChoices, ChoiceItem


class Priority(DjangoChoices):
    Low = ChoiceItem(1, 'Low')
    Medium = ChoiceItem(2, 'Medium')
    High = ChoiceItem(3, 'High')


class Column(DjangoChoices):
    One = ChoiceItem(1, 'One')
    Two = ChoiceItem(2, 'Two')
    Three = ChoiceItem(3, 'Three')


class Category(DjangoChoices):
    Analysis = ChoiceItem(1, 'Analysis')
    Development = ChoiceItem(2, 'Development')
    Testing = ChoiceItem(3, 'Testing')
    Implementation = ChoiceItem(4, 'Implementation')


class TaskStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    InProgress = ChoiceItem(2, 'In Progress')
    PartiallyDone = ChoiceItem(3, 'Partially Done')
    Done = ChoiceItem(4, 'Done')
    Delivered = ChoiceItem(5, 'Delivered')
    NotDone = ChoiceItem(6, 'Not Done')
    Rejected = ChoiceItem(7, 'Rejected')


class DeliverableStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    InProgress = ChoiceItem(2, 'In Progress')
    Done = ChoiceItem(3, 'Done')
    Delivered = ChoiceItem(4, 'Delivered')
    Rejected = ChoiceItem(5, 'Rejected')


class OverTimeStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    Acknowledged = ChoiceItem(2, 'Acknowledged')
    Done = ChoiceItem(3, 'Done')
    Rejected = ChoiceItem(4, 'Rejected')
