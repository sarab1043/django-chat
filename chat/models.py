from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    online = models.BooleanField(default = False)
    offline = models.BooleanField(default = False)
    last_seen = models.DateTimeField(null = True, blank = True)

class Room(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

class Group(models.Model):
    user = models.ForeignKey(User , on_delete= models.CASCADE,blank=True,null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


   
   