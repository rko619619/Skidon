from django.shortcuts import render
from about.models import Technology


def about(requests):
    return render(
        requests, "index.html", context={"technologies": Technology.objects.all()}
    )
