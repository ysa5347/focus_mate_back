from django.db import models
from account.models import CustomUser

class timeBlock(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='timeBlocks')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    application = models.CharField(max_length=50)
    ststus = models.SmallIntegerField()

    comment = models.CharField(max_length=200, blank=True)
    # livingArea = models.PointField()
    # 관심사

    class Meta:
        verbose_name = 'timeBlock'
        verbose_name_plural = 'timeBlocks'

    def __str__(self):
        return f'{self.user}; {self.endTime - self.startTime} timeBlock'

# Create your models here.
