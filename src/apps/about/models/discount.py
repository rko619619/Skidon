from django.db import models as m


class Discount(m.Model):
    shop = m.TextField(blank=True)
    name_of_discount = m.TextField(blank=True)
    text = m.TextField(blank=True, unique=True)
    price = m.TextField(blank=True)
    additional_media = m.URLField(blank=True)
    media = m.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Discount"
        ordering = ["shop"]

    def __repr__(self):
        return f"Shop # {self.pk}: '{self.media}'"

    def __str__(self):
        return f"{self.shop}: '{self.pk}'"
