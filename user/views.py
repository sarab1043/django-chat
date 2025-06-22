from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from chat.models import Profile
from django.contrib.auth import authenticate, login,logout
from django.conf import settings 

# Create your views here.
def signin(request):
    context={}
    if request.method == 'POST':
        username=request.POST['email']
        password=request.POST['password']
        user=authenticate(username=username,password= password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("/admin")
            else:
                return redirect('index')
        else:
            context['error']=f'Invalid credentials'
    return render(request,'signin.html',context)
   
def signup(request):
    context={}
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        email=request.POST['email']
       
        if User.objects.filter(username=email).exists():
            context['error']=f'user already exists'
        else:
            user = User.objects.create_user(email,email,password)
            user.first_name=name
            user.save()
            user_id  = User.objects.get(username = email)
            user_profile = Profile.objects.create(user = user_id)
            return redirect('signin')
    return render(request,'signup.html',context)
  
def signout(request):
    logout(request)
    return redirect('signin')

# def user_profile(request,id):
   
#     user = request.user
#     user_obj = User.objects.get(username = user)
#     firstname = user_obj.first_name

#     user_profile = Profile.objects.get(user = user_obj.id)
#     return render(request, "user_profile.html", {'user_obj' : user_obj, 'user_profile':user_profile})
