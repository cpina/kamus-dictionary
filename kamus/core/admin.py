from django.contrib import admin

from . import models


class LanguageAdmin(admin.ModelAdmin):
    search_fields = ("code", "name",)
    list_display = ("code", "name",)
    ordering = ("code", "name",)

class WordWithTranslationAdmin(admin.ModelAdmin):
    search_fields = ("word", "language",)
    list_display = ("word", "language",)
    ordering = ("word", "language",)



admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.WordWithTranslation, WordWithTranslationAdmin)
