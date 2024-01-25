from django.db import models
from account.models import CustomUser
from django.utils.translation import gettext_lazy as _

class groupSession(models.Model):
    name = models.SlugField(max_length=50)
    users = models.ManyToManyField(CustomUser, related_name="ptcpGroups", through='groupUserTable')
    gender = models.BooleanField(null=True)
    leader = models.ForeignKey(CustomUser, related_name="leadingGroups", on_delete=models.PROTECT)
    userPresent = models.SmallIntegerField(default=1)
    userCap = models.SmallIntegerField(default=1)
    isReady = models.BooleanField(default=False)
    createdTime = models.DateTimeField(auto_now_add=True)
    pubTime = models.DateTimeField(null=True)
    readyTime = models.DateTimeField(null=True)
    matchTime = models.DateTimeField(null=True)
    pubStat = models.BooleanField(default=False)
    matchStat = models.SmallIntegerField(default=0)

class groupUserTable(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="groupTable")
    userIsReady = models.BooleanField(default=False)
    # acceptStat = False(invited), True(Accept) 
    acceptStat = models.BooleanField(default=False)
    group = models.ForeignKey(groupSession, on_delete=models.CASCADE, related_name="userTable")