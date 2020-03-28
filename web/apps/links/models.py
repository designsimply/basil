from django.db import models
# Create your models here.


class Link(models.Model):
    url = models.URLField(
        help_text="URL of the link we care about.",
    )
    title = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True, editable=False,
    )
