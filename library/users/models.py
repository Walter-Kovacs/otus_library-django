from django.contrib.auth.models import User
from django.db import models

from books.models import Book


class LibraryAbstractUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=32)

    class Meta:
        abstract = True


class Reader(LibraryAbstractUser):
    books = models.ManyToManyField(Book)


class Librarian(LibraryAbstractUser):
    staff_number = models.CharField(max_length=8)

    @property
    def is_active(self):
        return self.staff_number != ''
