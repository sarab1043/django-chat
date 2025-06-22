from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.conf import settings 
from .models import Group
from .models import Room
from .models import Message
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

def index(request):
    return render(request, 'chat/index.html')

def invite_members(request):
    context={}
    if request.method=="POST":
        email=request.POST['email']
        room_name= request.session.get('room_name')
        if User.objects.filter(username=email).exists():
            subject = 'Join the chat room'
            message = f"Hi  , click on the link to join the chat   http://127.0.0.1:8000/chat/room/{room_name}/"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail( subject, message, email_from, recipient_list )
            context['success']=f'Email sent successfully'
            room = Room.objects.filter(name = room_name).first()
            user = User.objects.filter(email=email).first()
            group = Group.objects.create(user=user,room=room)
        else:
            context['error'] = f'User not exists!'
        group = Group.objects.all
        context['group'] = group
    return render(request, "chat/invite_members.html",context)

def room(request, room_name):
    rooms = Room.objects.all
    all_users = User.objects.all
    request.session['room_name'] = room_name
    if Room.objects.filter(name=room_name).exists():
        print("room exists")
    else:
        room=Room.objects.create(name=room_name)

    room=Room.objects.get(name=room_name)
    room_id=room.id
    room=Room.objects.get(id=room_id)
    id=room.id
    group = Group.objects.filter(room=room)
    messages = Message.objects.filter(room=room)
    user=request.user
    if user.is_authenticated:
        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'messages' : messages,
            'group' : group,
            'all_users':all_users,
            'rooms' : rooms
        })
    else:
        return redirect('signin')
    return render(request,'room.html')



