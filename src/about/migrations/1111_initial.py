# Generated by Django 3.0.3 on 2020-02-28 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.URLField(unique=True)),
                ('shop', models.TextField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Discount',
                'ordering': ['shop'],
            },
        ),
        migrations.CreateModel(
            name='Katalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(unique=True)),
                ('content', models.TextField(unique=True)),
                ('media', models.URLField(unique=True)),
                ('adress', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'katalog',
                'ordering': ['title'],
            },
        ),
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
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(unique=True)),
                ('content', models.TextField(unique=True)),
                ('media', models.URLField(unique=True)),
                ('at', models.DateField()),
                ('post_kateg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='about.Post_kateg')),
            ],
            options={
                'verbose_name_plural': 'post',
                'ordering': ['at', 'title'],
            },
        ),
    ]
