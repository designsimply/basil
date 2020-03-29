from django.contrib import admin

from links import models


class LinkTagInline(admin.TabularInline):
    model = models.LinkTag
    extra = 1


class LinkAdmin(admin.ModelAdmin):
    inlines = (LinkTagInline,)


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Link, LinkAdmin)
admin.site.register(models.Tag, TagAdmin)
