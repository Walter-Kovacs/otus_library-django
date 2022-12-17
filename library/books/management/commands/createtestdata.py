from django.core.management.base import BaseCommand

from books.models import (
    Author,
    Book,
)


class Command(BaseCommand):
    help = 'Creates test data in database.'

    jack_id: int
    noon_22century_id: int

    def handle(self, *args, **options):
        if not self.delete_existing_data():
            return

        print('Creating data ...')
        self.create_jack_data()
        self.create_noon_22century_data()
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
        Author.objects.all().delete()
        return True

    @classmethod
    def create_jack_data(cls):
        author = Author.objects.create(
            name='Jack London',
            about='John Griffith Chaney (January 12, 1876 – November 22, 1916)',
        )
        print(author.name)

        book = Book.objects.create(
            title='The Call of the Wild',
            abstract='A short adventure novel set in Yukon, Canada, during the 1890s Klondike Gold Rush.',
            amount=2,
        )
        author.books.add(book)
        print(book.title)

        book = Book.objects.create(
            title='White Fang',
            abstract="White Fang is the name of the book's eponymous character, a wild wolfdog.",
            amount=3,
        )
        author.books.add(book)
        print(book.title)
        
        author.save()

        cls.jack_id = author.id

    @classmethod
    def create_noon_22century_data(cls):
        arkadii = Author.objects.create(name='Аркадий Стругацкий')
        print(arkadii.name)

        boris = Author.objects.create(name='Борис Стругацкий')
        print(boris.name)

        book = Book.objects.create(
            title='Полдень, XXII век',
            amount=1,
        )
        arkadii.books.add(book)
        arkadii.save()
        boris.books.add(book)
        boris.save()
        print(book.title)

        cls.noon_22century_id = book.id

    @classmethod
    def show_created_data(cls):
        jack = Author.objects.get(id=cls.jack_id)
        print('-' * 50)
        print(jack.name)
        for book in jack.books.all():
            print(' ' * 4, book.title)

        noon_22century = Book.objects.get(id=cls.noon_22century_id)
        print('-' * 50)
        print(noon_22century.title)
        for author in noon_22century.author_set.all():
            print(' ' * 4, author.name)

        print('-' * 50)
