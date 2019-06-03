from djchoices import DjangoChoices, ChoiceItem


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
