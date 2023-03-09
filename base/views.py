from django.shortcuts import render,redirect,HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    datas = Room.objects.filter(Q(topic__name__contains=q) | 
    Q(name__icontains=q)|
    Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count= datas.count()
    
    room_messages = Message.objects.all()[:5]

    context = {'rooms':datas,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request, 'index.html',context)
    
def rooms(request,pk):
    rooms = Room.objects.get(id=pk)
    room_messages = rooms.message_set.all().order_by('-created')
    participants = rooms.participants.all()

    context ={'rooms':rooms,'room_messages':room_messages,'participants':participants}

    if request.method == "POST":
        body=request.POST.get('body')
        message= Message.objects.create(
            user=request.user,room=rooms,body=body
        )
        return redirect('room',pk=rooms.id)

    return render(request,'room.html',context)
@login_required(login_url='loginPage')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'room_form.html',context)
@login_required(login_url='loginPage')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You are not authenticated")
    context={'form':form}
    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'room_form.html',context)
@login_required(login_url='loginPage')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    if request.user != room.host:
        return HttpResponse("You are not authenticated")
    else:
        return render(request,'delete.html')
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(User.objects.all())
        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request,"User doesnot exists")
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return  redirect('home')



    context={}
    return render(request,'login_register.html',context)
@login_required(login_url='loginPage')
def logoutUser(request):
    logout(request)
    return redirect('home')

def Userprofile(request,pk):
    user= User.objects.get(id=pk)
    context ={'user':user}

    return render(request,'profile.html',context)
def topics(request):
    return render(request,'index.html')