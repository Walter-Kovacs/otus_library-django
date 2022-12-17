from django.core.validators import MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=32, unique=True)


class WrittenWork(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    description = models.TextField(blank=True)


class Author(models.Model):
    name = models.CharField(max_length=64, unique=True)
    about = models.TextField(blank=True)
    works = models.ManyToManyField(WrittenWork)


class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Book(models.Model):
    title = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    publishing_year = models.IntegerField()
    abstract = models.TextField(blank=True)
    works = models.ManyToManyField(WrittenWork)
    amount = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(limit_value=0),
        ],
    )
