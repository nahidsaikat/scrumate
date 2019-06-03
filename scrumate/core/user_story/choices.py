from djchoices import DjangoChoices, ChoiceItem


class UserStoryStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    Analysing = ChoiceItem(2, 'Analysing')
    AnalysisComplete = ChoiceItem(3, 'Analysis Complete')
    Developing = ChoiceItem(4, 'Developing')
    DevelopmentComplete = ChoiceItem(5, 'Development Complete')
    Delivered = ChoiceItem(6, 'Delivered')
