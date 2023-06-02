from django.conf import settings
from django.db import models


class URL(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    url = models.URLField(verbose_name="URL")
    paused = models.BooleanField(default=False)

    class Meta:
        unique_together = "user", "url"

    def __str__(self):
        return self.url
