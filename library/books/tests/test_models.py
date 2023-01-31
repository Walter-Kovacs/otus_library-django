from django.test import TestCase
from faker import Faker
from mixer.backend.django import mixer

from books.models import (
    Author,
    Book,
    BookCopy,
    Genre,
    Publisher,
    WrittenWork,
)
from users.models import Reader


class TestGenreModel(TestCase):

    def setUp(self) -> None:
        faker = Faker()
        genre_names = faker.words(nb=13, unique=True)
        for name in genre_names:
            Genre.objects.create(name=name)

    def tearDown(self) -> None:
        Genre.objects.all().delete()

    def test_str(self):
        genres = Genre.objects.all()
        for genre in genres:
            self.assertEqual(str(genre), genre.name)

    def test_ordering(self):
        genres = Genre.objects.all()
        genre_names = [g.name for g in genres]
        sorted_genre_names = sorted(genre_names)
        self.assertListEqual(genre_names, sorted_genre_names)


class TestWrittenWorkModel(TestCase):

    def setUp(self) -> None:
        num_of_works = 13
        faker = Faker()
        titles = faker.words(nb=num_of_works, unique=True)
        mixer.cycle(num_of_works).blend(WrittenWork, title=(t for t in titles))

    def tearDown(self) -> None:
        WrittenWork.objects.all().delete()
        Genre.objects.all().delete()

    def test_str(self):
        works = WrittenWork.objects.all()
        for work in works:
            self.assertEqual(str(work), work.title)

    def test_ordering(self):
        works = WrittenWork.objects.all()
        titles = [work.title for work in works]
        sorted_titles = sorted(titles)
        self.assertListEqual(titles, sorted_titles)


class TestAuthorModel(TestCase):

    def setUp(self) -> None:
        num_of_authors = 13
        faker = Faker()
        names = [faker.unique.name() for i in range(num_of_authors)]
        mixer.cycle(num_of_authors).blend(Author, name=(name for name in names))

    def tearDown(self) -> None:
        Author.objects.all().delete()

    def test_str(self):
        authors = Author.objects.all()
        for author in authors:
            self.assertEqual(str(author), author.name)

    def test_ordering(self):
        authors = Author.objects.all()
        names = [author.name for author in authors]
        sorted_names = sorted(names)
        self.assertListEqual(names, sorted_names)


class TestPublisherModel(TestCase):

    def setUp(self) -> None:
        num_of_publishers = 13
        faker = Faker()
        names = [faker.unique.company() for i in range(num_of_publishers)]
        mixer.cycle(num_of_publishers).blend(Publisher, name=(name for name in names))

    def tearDown(self) -> None:
        Publisher.objects.all().delete()

    def test_str(self):
        publishers = Publisher.objects.all()
        for p in publishers:
            self.assertEqual(str(p), p.name)

    def test_ordering(self):
        publishers = Publisher.objects.all()
        names = [p.name for p in publishers]
        sorted_names = sorted(names)
        self.assertListEqual(names, sorted_names)


class TestBookModel(TestCase):

    def setUp(self) -> None:
        num_of_books = 13
        faker = Faker()
        titles = [faker.unique.catch_phrase() for i in range(num_of_books)]
        mixer.cycle(num_of_books).blend(Book, title=(title for title in titles))

    def tearDown(self) -> None:
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        WrittenWork.objects.all().delete()
        Genre.objects.all().delete()

    def test_str(self):
        books = Book.objects.all()
        for book in books:
            self.assertEqual(
                str(book),
                f'{book.title} ({book.publisher}, {book.publishing_year})'
            )

    def test_ordering(self):
        books = Book.objects.all()
        titles = [book.title for book in books]
        sorted_titles = sorted(titles)
        self.assertListEqual(titles, sorted_titles)


class TestBookCopyModel(TestCase):
    number_of_storage_copies = 3
    number_of_lend_copies = 2

    def setUp(self) -> None:
        self.reader = mixer.blend(Reader)
        mixer.cycle(TestBookCopyModel.number_of_storage_copies).blend(BookCopy, reader=None)
        mixer.cycle(TestBookCopyModel.number_of_lend_copies).blend(BookCopy, reader=self.reader)

    def tearDown(self) -> None:
        BookCopy.objects.all().delete()
        Reader.objects.all().delete()

    def test_number_of_all_copies(self):
        self.assertEqual(
            BookCopy.number_all(),
            TestBookCopyModel.number_of_storage_copies + TestBookCopyModel.number_of_lend_copies
        )

    def test_number_of_storage_copies(self):
        self.assertEqual(BookCopy.number_in_storage(), TestBookCopyModel.number_of_storage_copies)

    def test_number_of_lend_copies(self):
        self.assertEqual(BookCopy.number_lend(), TestBookCopyModel.number_of_lend_copies)

    def test_number_check_sum(self):
        self.assertEqual(
            BookCopy.number_all(),
            BookCopy.number_in_storage() + BookCopy.number_lend()
        )

    def test_storage_copies(self):
        copies = BookCopy.objects.filter(reader__isnull=True)
        self.assertListEqual(
            list(copies),
            list(BookCopy.storage_copies())
        )

    def test_lend_copies(self):
        copies = BookCopy.objects.filter(reader__isnull=False)
        self.assertListEqual(
            list(copies),
            list(BookCopy.lend_copies())
        )
