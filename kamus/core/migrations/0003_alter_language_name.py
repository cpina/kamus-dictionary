# Generated by Django 4.1 on 2022-08-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_wordwithtranslation_word"),
    ]

    operations = [
        migrations.AlterField(
            model_name="language",
            name="name",
            field=models.CharField(max_length=25),
        ),
    ]
