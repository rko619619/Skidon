from django.shortcuts import render

from platform import system


def about(request):
    return render(
        request,
        "index.html",
        {
            "data": [
                "Skidon project",
                system(),
            ]
        },
    )
