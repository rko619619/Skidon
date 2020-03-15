# Generated by Django 3.0.4 on 2020-03-12 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("about", "1113_auto_20200309_2333")]

    operations = [
        migrations.AlterModelOptions(
            name="katalog",
            options={
                "ordering": ["id", "title", "content", "media", "adress"],
                "verbose_name_plural": "katalog",
            },
        ),
        migrations.AlterField(
            model_name="discount", name="media", field=models.URLField()
        ),
        migrations.AlterField(
            model_name="discount", name="shop", field=models.TextField()
        ),
    ]
