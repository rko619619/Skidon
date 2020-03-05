from django.views.generic import ListView

from apps.about.models import Katalog


class AboutView(ListView):
    model=Katalog
    template_name = "about/index.html"