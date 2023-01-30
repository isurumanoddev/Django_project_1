from django.shortcuts import render,redirect
from .models import Room
from .forms import RoomForm


# Create your views here.
def home(request):
    rooms = Room.objects.all()
    return render(request, "home.html", {'rooms': rooms})


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}

    return render(request, "room.html", context)


def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "room_form.html", context)

