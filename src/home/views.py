from django.shortcuts import render

from platform import system


def actual(request):
    return render(request, "home/templates/home/index.html", {"data": ["Skidon project", system()]})
