from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


def login_page(request):
    page = "login_page"
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

    context = {"page": page}
    return render(request, "login_register.html", context)


def logout_user(request):
    logout(request)
    return redirect("home")


def user_register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("user registered")
            return redirect("login")

    context = {"form": form}
    return render(request, "login_register.html", context)


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
    room_messages = room.message_set.all()
    print(room_messages)
    if request.method == "POST":
        messages = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("comment")

        )
        return redirect("room",pk=room.id)


    context = {"room": room, "room_messages": room_messages}

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
