from django.views.generic import TemplateView
<<<<<<< HEAD

from about.models import Discount
from about.models import Katalog


class AboutView(TemplateView):
    http_method_names = ("get", "post")
=======
from about.models import Katalog, Discount, Post_kateg

class AboutView(TemplateView):
    #http_method_names =('get','post')
>>>>>>> master

    template_name = "about/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

<<<<<<< HEAD
        context["Katalog"] = Katalog.objects.all()
        context["Discount"] = Discount.objects.all()
        context["Post_kateg"] = Discount.objects.all()
=======
        context["Katalog"]= Katalog.objects.all()
        context["Discount"]= Discount.objects.all()
        context["Post_kateg"]=Post_kateg.objects.all()

>>>>>>> master

        return context
