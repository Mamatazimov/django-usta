from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core import validators

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    user_status = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    

    def __str__(self):
        return self.username

    class Meta:
        abstract = False
