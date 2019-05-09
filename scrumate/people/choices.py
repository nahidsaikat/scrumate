from djchoices import DjangoChoices, ChoiceItem


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
