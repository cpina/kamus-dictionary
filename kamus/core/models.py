from django.db import models

class Language(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class WordWithTranslation(models.Model):
    word = models.CharField(max_length=100, db_index=True)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    # TODO: no constraints with unique_index. To be explained.

    def __str__(self):
        return f"{self.word}-{self.language}"
