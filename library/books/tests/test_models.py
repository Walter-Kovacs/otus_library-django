from django.test import TestCase
from faker import Faker
from mixer.backend.django import mixer

from books.models import (
    Author,
    Genre,
    Publisher,
    WrittenWork,
)


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
