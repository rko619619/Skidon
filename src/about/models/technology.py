from django.db import models as m


class Technology(m.Model):
    name = m.TextField(unique=True)
    url = m.URLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "techologies"
