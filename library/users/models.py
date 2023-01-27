from django.contrib.auth.models import User
from django.db import models


class LibraryAbstractUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=32)

    class Meta:
        abstract = True


class Reader(LibraryAbstractUser):
    pass


class Librarian(LibraryAbstractUser):
    staff_number = models.CharField(max_length=8)

    @property
    def is_active(self):
        return self.staff_number != ''
