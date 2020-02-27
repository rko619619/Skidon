from django.db import models as m


class Katalog(m.Model):
    title = m.TextField(unique=True)
    content = m.TextField(unique=True)
    media = m.URLField(unique=True)
    adress = m.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "katalog"
        ordering = ["title"]

    def __repr__(self):
        return f"Zavedeniya # {self.pk}: '{self.title}'"

    def __str__(self):
        return f"{self.pk}: '{self.title}'"
