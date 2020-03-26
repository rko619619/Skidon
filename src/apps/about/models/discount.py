from django.db import models as m


class Discount(m.Model):
    shop = m.TextField()
    name_of_discount = m.TextField(unique=True)
    text = m.TextField()
    price = m.TextField()
    additional_media = m.URLField()
    media = m.URLField()


    class Meta:
        verbose_name_plural = "Discount"
        ordering = ["shop"]

    def __repr__(self):
        return f"Shop # {self.pk}: '{self.media}'"

    def __str__(self):
        return f"{self.shop}: '{self.pk}'"
