from django.db import models as m


class Post_kateg(m.Model):
    name = m.TextField(unique=True)
    class Meta:
        verbose_name_plural = "Post_kateg"
        ordering = ["name"]

    def __repr__(self):
        return f"{self.__class__.__name__} # '{self.pk}:{self.name}'"

    def __str__(self):
        return f"{self.name}: '{self.pk}'"
