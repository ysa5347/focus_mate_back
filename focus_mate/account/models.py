from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, userID, password, **extra_fields):
        if not userID:
            raise ValueError('The given ID must be set')
        user = self.model(userID=userID, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, userID, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(userID, password, **extra_fields)

    def create_superuser(self, userID, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(userID, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin): #AbstractBaseUser에 password columm이 이미 있음
    userID = models.CharField(max_length=15, primary_key=True, help_text='user ID')
    createdTime = models.DateTimeField(_('date joined'), default=timezone.now)
    comment = models.CharField(max_length=200, blank=True)
    outScreen = models.IntegerField(default=60)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    objects = UserManager()

    USERNAME_FIELD = 'userID'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.userID}'

    def get_short_name(self):
        return self.userID

class category(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='categories')
    apps = models.ManyToManyField('app', related_name='categories')
    category = models.CharField(max_length=50)

class app(models.Model):
    platform = models.CharField(max_length=50)
    app = models.CharField(max_length=50)
