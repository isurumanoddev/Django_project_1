from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # print(username,password)
        try:
            User.objects.get(username=username)

        except:
            print("NOT exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            print("User not registered")

    return render(request, "login_register.html")


def logout_user(request):
    logout(request)
    return redirect("home")


def home(request):
    if request.GET.get("q") is not None:
        q = request.GET.get("q")
    else:
        q = ""

    rooms = Room.objects.filter(topic__name__icontains=q)
    room_count = rooms.count()

    topics = Topic.objects.all()
    context = {'rooms': rooms, "topics": topics, "room_count": room_count}
    return render(request, "home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}

    return render(request, "room.html", context)


@login_required(login_url="login")
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "room_form.html", context)


@login_required(login_url="login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("you cannot update another user room")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")


    context = {"form": form}
    return render(request, "room_form.html", context)


@login_required(login_url="login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("you cannot delete another user room")
    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "delete.html", {"obj": room})
