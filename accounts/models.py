from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile


class KcupUserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='gamer_profile')
