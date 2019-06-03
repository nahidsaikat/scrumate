from djchoices import DjangoChoices, ChoiceItem


class Priority(DjangoChoices):
    Low = ChoiceItem(1, 'Low')
    Medium = ChoiceItem(2, 'Medium')
    High = ChoiceItem(3, 'High')


class Column(DjangoChoices):
    One = ChoiceItem(1, 'One')
    Two = ChoiceItem(2, 'Two')
    Three = ChoiceItem(3, 'Three')
