from django.db import models
# from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone


# Create your models here.

# class CustomUser(AbstractUser):
#     address = models.TextField(null=True, blank=True)

def getday():
    date = timezone.now()
    day = datetime.strftime(date, "%a-%d-%b-%Y")
    return(day)


class Todo(models.Model):
    date = models.CharField(default=getday, max_length=50)
    title = models.CharField(max_length=250)
    body = models.TextField()
    


    def __str__(self):
        return self.title
