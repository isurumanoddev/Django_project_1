from django.shortcuts import render
from .models import Room
#
# rooms = [
#     {"id": 1, "name": "Lets learn something"},
#     {"id": 2, "name": "Deeper learn something"},
#     {"id": 3, "name": "Front matter "},
#     {"id": 4, "name": "Front matter "},
#     {"id": 5, "name": "Front matter "},
#     {"id": 6, "name": "Front matter "},
#     {"id": 7, "name": "Front matter "}
# ]


# Create your views here.
def home(request):
    rooms = Room.objects.all()
    return render(request, "home.html", {'rooms': rooms})


def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}

    return render(request, "room.html", context)
