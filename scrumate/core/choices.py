from djchoices import DjangoChoices, ChoiceItem


class OverTimeStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    Acknowledged = ChoiceItem(2, 'Acknowledged')
    Done = ChoiceItem(3, 'Done')
    Rejected = ChoiceItem(4, 'Rejected')
