from django.db import models

# Create your models here.
class Vacancy(models.Model):
    name = models.CharField(max_length=120)
    short_description = models.TextField()
    salary_from = models.IntegerField(null=True)
    salary_to = models.IntegerField(null=True)
    currency = models.CharField(max_length=3)
    link = models.TextField()
