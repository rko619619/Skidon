# Generated by Django 3.0.3 on 2020-02-19 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '1001_auto_20200219_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_kateg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Post_kateg',
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='katalog',
            options={'ordering': ['title'], 'verbose_name_plural': 'katalog'},
        ),
    ]