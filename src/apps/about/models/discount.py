from django.db import models as m


class Discount(m.Model):
    media = m.URLField()
    shop = m.TextField()

    class Meta:
        verbose_name_plural = "Discount"
        ordering = ["media"]

    def __repr__(self):
        return f"Shop # {self.pk}: '{self.media}'"

    def __str__(self):
        return f"{self.shop}: '{self.pk}'"
