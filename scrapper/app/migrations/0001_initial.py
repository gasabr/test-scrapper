# Generated by Django 2.0 on 2019-04-14 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('short_description', models.TextField()),
                ('salary_from', models.IntegerField(null=True)),
                ('salary_to', models.IntegerField(null=True)),
                ('currency', models.CharField(max_length=3)),
                ('link', models.TextField()),
            ],
        ),
    ]
