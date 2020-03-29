from django.db import models

from common import TimestampMixin


class Link(TimestampMixin, models.Model):
    url = models.URLField(
        help_text="URL of the link we care about.",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', through='LinkTag')

    def __str__(self):
        return f'{self.title}'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    links = models.ManyToManyField('Link', through='LinkTag')

    def __str__(self):
        return f'{self.name}'


class LinkTag(TimestampMixin, models.Model):
    """ Many-to-many relationship of Link to Tag """
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    link = models.ForeignKey('Link', on_delete=models.CASCADE)
