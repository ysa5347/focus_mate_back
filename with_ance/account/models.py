
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, userID, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not userID:
            raise ValueError('The given ID must be set')
        email = self.normalize_email(email)
        user = self.model(userID=userID, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, userID, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(userID, email, password, **extra_fields)

    def create_superuser(self, userID, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(userID, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin): #AbstractBaseUser에 password columm이 이미 있음
    userID = models.CharField(max_length=15, primary_key=True, help_text='user ID')
    phoneNum = models.CharField(max_length=11, unique=True, help_text='phone number')
    gender = models.BooleanField(null=True)
    email = models.CharField(max_length=100, unique=True, help_text='Email')
    birth = models.PositiveSmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=40, null=True) 
    createdTime = models.DateTimeField(_('date joined'), default=timezone.now)
    college = models.CharField(max_length=100, null=True)
    major = models.CharField(max_length=100, null=True)
    semaster = models.PositiveSmallIntegerField(null=True)
    comment = models.CharField(max_length=200, blank=True)
    profileImg = models.ImageField(blank=True)
    # livingArea = models.PointField()
    # groups => related_name = 
    # rooms => related_name = 
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    objects = UserManager()

    REQUIRED_FIELDS = ['email']
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'userID'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.userID}'

    def get_short_name(self):
        return self.userID
    
class FollowUserStat(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower_user')        # 팔로우 당한사람
    follow = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follow_user')            # 팔로우 하는사람


# Create your models here.
