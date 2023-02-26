from django.db import models

from users.models import Reader


class Genre(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class WrittenWork(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)

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

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return f'{self.title} ({self.publisher.name}, {self.publishing_year})'


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    inventory_number = models.CharField(max_length=16, unique=True)
    reader = models.ForeignKey(Reader, on_delete=models.PROTECT, blank=True, null=True)
    reader_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('book', )

    def __str__(self):
        return self.inventory_number

    @staticmethod
    def number_all(book_id: int) -> int:
        return BookCopy.objects.filter(book__id=book_id).count()

    @staticmethod
    def number_in_storage(book_id: int) -> int:
        return BookCopy.objects.filter(book__id=book_id, reader__isnull=True).count()

    @staticmethod
    def number_lend(book_id: int) -> int:
        return BookCopy.objects.filter(book__id=book_id, reader__isnull=False).count()

    @staticmethod
    def storage_copies(book_id: int):
        return BookCopy.objects.filter(book__id=book_id, reader__isnull=True)

    @staticmethod
    def lend_copies(book_id: int):
        return BookCopy.objects.filter(book__id=book_id, reader__isnull=False)


class BookRequest(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    reader = models.ForeignKey(Reader, on_delete=models.PROTECT)

    class Meta:
        ordering = ('book', )
