from django.db import models
from django.conf import settings

class Item(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name