from django.urls import include, path


urlpatterns = [path("", include("apps.api.impl.urls"))]
