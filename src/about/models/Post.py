from django.db import models as m

<<<<<<< HEAD
from about.models import Post_kateg
=======
from about.models.post_kateg import Post_kateg

>>>>>>> master


class Post(m.Model):
    title = m.TextField(unique=True)
    content = m.TextField(unique=True)
    media = m.URLField(unique=True)
    at = m.DateField()
<<<<<<< HEAD

    post_kateg = m.ForeignKey(Post_kateg, on_delete=m.PROTECT)

    class Meta:
        verbose_name_plural = "post"
        ordering = ["at, title"]

    def __repr__(self):
        return f"{self.__class__.__name__}#{self.pk}:{self.post_kateg}"

    def __str__(self):
        return f"{self.title}:({self.post_kateg})"
=======
    post_kateg=m.ForeignKey(Post_kateg, on_delete=m.PROTECT)

    class Meta:
        verbose_name_plural ="post"
        ordering = ["at","title"]

    def __repr__(self):
        return f"{self.__class__.__name__}#{self.pk}:{self.title}"

    def __str__(self):
        return f"{self.title}:({self.title})"
>>>>>>> master
