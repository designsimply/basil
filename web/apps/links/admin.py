from django.contrib import admin

from links import models


class LinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Link, LinkAdmin)
