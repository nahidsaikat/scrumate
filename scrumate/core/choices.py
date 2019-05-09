from django.utils.translation import gettext as _
from djchoices import DjangoChoices, ChoiceItem


class ProjectStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    InProgress = ChoiceItem(2, 'In Progress')
    Completed = ChoiceItem(3, 'Completed')


class ProjectType(DjangoChoices):
    Public = ChoiceItem(1, 'Public')
    Private = ChoiceItem(2, 'Private')
    InHouse = ChoiceItem(3, 'In House')


class Priority(DjangoChoices):
    Low = ChoiceItem(1, 'Low')
    Medium = ChoiceItem(2, 'Medium')
    High = ChoiceItem(3, 'High')


class UserStoryStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    Analysing = ChoiceItem(2, 'Analysing')
    AnalysisComplete = ChoiceItem(3, 'Analysis Complete')
    Developing = ChoiceItem(4, 'Developing')
    DevelopmentComplete = ChoiceItem(5, 'Development Complete')
    Delivered = ChoiceItem(6, 'Delivered')


class SprintStatus(DjangoChoices):
    Pending = ChoiceItem(1, 'Pending')
    OnGoing = ChoiceItem(2, 'On Going')
    Completed = ChoiceItem(3, 'Completed')


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


class PartyType(DjangoChoices):
    Employee = ChoiceItem(1, 'Employee')
    Customer = ChoiceItem(2, 'Customer')
    Vendor = ChoiceItem(3, 'Vendor')


class PartySubType(DjangoChoices):
    Individual = ChoiceItem(1, 'Individual')
    Organization = ChoiceItem(2, 'Organization')


class PartyGender(DjangoChoices):
    Male = ChoiceItem(1, 'Male')
    Female = ChoiceItem(2, 'Female')


class PartyTitle(DjangoChoices):
    Mr = ChoiceItem(1, 'Mr.')
    Mrs = ChoiceItem(2, 'Mrs.')
    Miss = ChoiceItem(3, 'Miss')
