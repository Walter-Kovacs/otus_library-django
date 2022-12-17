from django.core.management.base import BaseCommand

from books.models import (
    Author,
    Book,
    Genre,
    Publisher,
    WrittenWork,
)


class Command(BaseCommand):
    help = 'Creates test data in database.'

    genres: dict = dict()
    works: dict = dict()
    book_id: int

    def handle(self, *args, **options):
        if not self.delete_existing_data():
            return

        print('Creating data ...')
        self.create_genre()
        self.create_jack_data()
        self.create_noon_22century_data()
        self.create_book()
        print('Data created.')

        self.show_created_data()

    @staticmethod
    def delete_existing_data() -> bool:
        confirmation: str = input(
            'You are trying to delete all data in db and create new test data.\n'
            'Proceed [yes/no]? '
        )
        if confirmation.lower() != 'yes':
            return False

        print('Deleting existing data ...')
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Author.objects.all().delete()
        WrittenWork.objects.all().delete()
        Genre.objects.all().delete()
        return True

    @classmethod
    def create_genre(cls):
        for name in ['Novel', 'Short novel', 'Short story']:
            genre = Genre.objects.create(name=name)
            cls.genres[name] = genre
            print('genre: ', genre.name)

    @classmethod
    def create_jack_data(cls):
        author = Author.objects.create(
            name='Jack London',
            about='John Griffith Chaney (January 12, 1876 – November 22, 1916)',
        )
        print('author:', author.name)

        works_data = [
            {
                'title': 'The Call of the Wild',
                'genre': cls.genres['Short novel'],
                'description': 'A short adventure novel set in Yukon, Canada, during the 1890s Klondike Gold Rush.',
            },
            {
                'title': 'White Fang',
                'genre': cls.genres['Novel'],
                'description': "White Fang is the name of the book's eponymous character, a wild wolfdog.",
            },
        ]
        for data in works_data:
            work = WrittenWork.objects.create(**data)
            author.works.add(work)
            cls.works[data['title']] = work
            print('work:', work.title)

        author.save()

    @classmethod
    def create_noon_22century_data(cls):
        arkadii = Author.objects.create(name='Аркадий Стругацкий')
        print('author:', arkadii.name)

        boris = Author.objects.create(name='Борис Стругацкий')
        print('author:', boris.name)

        work = WrittenWork.objects.create(
            title='Полдень, XXII век',
            genre=cls.genres['Novel']
        )
        cls.works[work.title] = work
        print('work:', work.title)

        arkadii.works.add(work)
        arkadii.save()
        boris.works.add(work)
        boris.save()

    @classmethod
    def create_book(cls):
        publisher = Publisher.objects.create(name='Kovacs And Friends Publications')
        print('publisher:', publisher.name)

        book = Book.objects.create(
            title='Home reading, volume 1',
            publisher=publisher,
            publishing_year=2022,
            abstract='Collection of novels',
            amount=2,
        )
        cls.book_id = book.id
        print('book:', book.title)

        for work_title in cls.works:
            book.works.add(cls.works[work_title])
        book.save()

    @classmethod
    def show_created_data(cls):
        print('-' * 50)
        book = Book.objects.get(id=cls.book_id)
        print(f'"{book.title}" ({book.abstract}), {book.publisher.name}, {book.publishing_year}, amount: {book.amount})')

        for work in book.works.all():
            print(' ' * 4, f'"{work.title}", {work.genre.name}')
            for author in work.author_set.all():
                print(' ' * 8, author.name)

        print('-' * 50)
