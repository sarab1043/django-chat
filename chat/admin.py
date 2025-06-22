from django.contrib import admin
from .models import Message,Room,Group

# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id','message']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['id' , 'room']

admin.site.register(Message,MessageAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(Group,GroupAdmin)
