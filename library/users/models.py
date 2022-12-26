from django.contrib.auth.models import User
from django.db import models

from books.models import Book


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=32)
    books = models.ManyToManyField(Book)
