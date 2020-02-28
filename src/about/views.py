from django.views.generic import TemplateView
from about.models import Katalog, Discount, Post_kateg, Post

class AboutView(TemplateView):
    http_method_names =('get','post')


    template_name = "about/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context["Katalog"]= Katalog.objects.all()
        context["Discount"]= Discount.objects.all()
        context["Post_kateg"]=Post_kateg.objects.all()
        context["Post"] = Post.objects.all()


        return context
