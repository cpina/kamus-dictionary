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

class ImportedAdmin(admin.ModelAdmin):
    search_fields = ("language", "imported_on", "translated_words", "total_words", "file_path", "file_created_on", "file_size")
    list_display = ("language", "imported_on", "translated_words", "total_words", "file_path", "file_created_on", "file_size")
    ordering = ("language", "imported_on", "translated_words", "total_words", "file_path", "file_created_on", "file_size")


admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.WordWithTranslation, WordWithTranslationAdmin)
admin.site.register(models.Import, ImportedAdmin)
