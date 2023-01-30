from django.shortcuts import render

rooms = [
    {"id": 1, "name": "Lets learn something"},
    {"id": 2, "name": "Deeper learn something"},
    {"id": 3, "name": "Front matter "},
    {"id": 4, "name": "Front matter "},
    {"id": 5, "name": "Front matter "},
    {"id": 6, "name": "Front matter "},
    {"id": 7, "name": "Front matter "}
]


# Create your views here.
def home(request):
    return render(request, "home.html", {'rooms': rooms})


def room(request,pk):
    room = None
    for i in rooms:
        if i["id"] == int(pk):
            room = i
            print("fount")

    context = {"room": room}

    return render(request, "about.html",context)
