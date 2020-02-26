from django.db import models as m

from about.models import Post_kateg


class Post(m.Model):
    title = m.TextField(unique=True)
    content = m.TextField(unique=True)
    media = m.URLField(unique=True)
    at = m.DateField()
    post_kateg = m.ForeignKey(Post_kateg, on_delete=m.PROTECT)

    class Meta:
        verbose_name_plural = "post"
        ordering = ["at, title"]

        def __repr__(self):
            return f"{self.__class__.name__}#{self.pk}:{self.title}"

        def __str__(self):
            return f"{self.title}:({self.title})"
