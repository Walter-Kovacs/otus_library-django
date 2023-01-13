from django.core.validators import MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class WrittenWork(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=64, unique=True)
    about = models.TextField(blank=True)
    works = models.ManyToManyField(WrittenWork)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


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

    class Meta:
        ordering = ('title', )
