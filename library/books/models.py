from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True)
    amount = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(limit_value=0),
        ],
    )


class Author(models.Model):
    name = models.CharField(max_length=64, unique=True)
    about = models.TextField(blank=True)
    books = models.ManyToManyField(Book)
