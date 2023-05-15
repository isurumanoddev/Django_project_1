from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


def login_page(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

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

    context = {}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    return redirect("home")


def user_register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("login")

    context = {"form": form}
    return render(request, "signup.html", context)


def home(request):
    if request.GET.get("q") is not None:
        q = request.GET.get("q")
    else:
        q = ""

    rooms = Room.objects.filter(topic__name__icontains=q)
    room_count = rooms.count()

    topics = Topic.objects.all()
    messages = Message.objects.filter(room__topic__name__icontains=q)
    context = {'rooms': rooms, "topics": topics, "room_count": room_count, "messages": messages}
    return render(request, "index.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST":
        messages = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("comment")

        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)

    context = {"room": room, "room_messages": room_messages, "participants": participants}

    return render(request, "room.html", context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    messages = user.message_set.all()
    rooms = user.room_set.all()

    context = {"user": user, "messages": messages, "rooms": rooms}
    return render(request, "profile.html", context)


@login_required(login_url="login")
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "create-room.html", context)


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
    return render(request, "create-room.html", context)


@login_required(login_url="login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("you cannot delete another user room")
    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "delete.html", {"obj": room})


@login_required(login_url="login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("you cannot delete another user room")
    if request.method == "POST":
        message.delete()
        return redirect("home")

    return render(request, "delete.html", {"obj": message})
