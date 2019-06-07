# default_app_config = 'scrumate.general.GeneralConfig'

from actstream import registry
from django.contrib.auth import get_user_model

User = get_user_model()
registry.register(User)
