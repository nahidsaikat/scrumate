from djchoices import DjangoChoices, ChoiceItem


class SprintStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    OnGoing = ChoiceItem(2, 'On Going')
    Completed = ChoiceItem(3, 'Completed')
