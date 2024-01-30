from django.db import models
from account.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def userPresentValidator(self, num):
    if num > self.userCap:
        raise ValidationError("정원 초과입니다.")

class groupSession(models.Model):
    name = models.SlugField(max_length=50)
    user = models.ManyToManyField(CustomUser, related_name="group", through='groupUserTable', through_fields=("group", "user"))
    gender = models.BooleanField(null=True)
    leaders = models.ManyToManyField(CustomUser, related_name="leadingGroups")
    userPresent = models.SmallIntegerField(default=1, validators=[userPresentValidator])
    userCap = models.SmallIntegerField(default=1)
    isReady = models.BooleanField(default=False)
    createdTime = models.DateTimeField(auto_now_add=True)
    pubTime = models.DateTimeField(null=True)
    readyTime = models.DateTimeField(null=True)
    matchTime = models.DateTimeField(null=True)
    pubStat = models.BooleanField(default=False)
    matchStat = models.SmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        # tableNum = groupUserTable.objects.filter(group=self, acceptStat=True).count()
        # if self.userPresent != tableNum:
        #     raise ValidationError(f"API exception, group args 'userPresent' not match with groupUserTable QuerySet count. userPresent: {self.userPresent} Table Count: {tableNum}")
        # if self.userPresent > self.userCap:
        #     raise ValidationError(f"Validation error, the group is full.{self.userPresent}/{self.userCap}")
        super(groupSession, self).save(*args, **kwargs)
    # @property
    # def userPresent(self):

class groupUserTable(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(groupSession, on_delete=models.CASCADE)
    lastGroup = models.ForeignKey(groupSession, on_delete=models.CASCADE, null=True, default=None) #해당 유저의 매칭 이전 group
    acceptStat = models.BooleanField(default=False)
    acceptType = models.BooleanField(default=False) # False -> Target group이 초대한 경우. True -> Target group에 신청한 경우
    userIsReady = models.BooleanField(default=False)