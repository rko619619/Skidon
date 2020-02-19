from django.views.generic import TemplateView
from about.models import Katalog,Discount

class AboutView(TemplateView):
    http_method_names =('get','post')

    template_name="about/template/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["Katalog"]= Katalog.objects.all()
        context["Discount"]= Discount.objects.all()

        return context

