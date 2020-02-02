from django.shortcuts import render

from platform import system


def actual(request):
    return render(request, "home/index.html", {"data": ["Skidon project", system()]})
