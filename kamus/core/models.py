from django.db import models

class Language(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name

class WordWithTranslation(models.Model):
    word = models.CharField(max_length=100, db_collation="utf8_bin")
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["word", "language"],
                                    name="unique-word-code")
        ]

    def __str__(self):
        return f"{self.word}-{self.language}"
