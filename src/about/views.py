from django.views.generic import TemplateView
from about.models import katalog, discount, post_kateg

class AboutView(TemplateView):
    http_method_names =('get','post')


    template_name = "about/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context["Katalog"]= katalog.objects.all()
        context["Discount"]= discount.objects.all()
        context["Post_kateg"]=post_kateg.objects.all()
        return context
