"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from books import views as book_views
from users import views as user_views

urlpatterns = [
    path('', book_views.welcome, name='welcome'),

    path('genres/', book_views.genre.GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', book_views.genre.GenreDetailView.as_view(), name='genre-details'),

    path('works/', book_views.work.WrittenWorkListView.as_view(), name='work-list'),
    path('works/<int:pk>/', book_views.work.WrittenWorkDetailView.as_view(), name='work-details'),

    path('authors/', book_views.author.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', book_views.author.AuthorDetailView.as_view(), name='author-details'),

    path('books/', book_views.book.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', book_views.book.BookDetailView.as_view(), name='book-details'),
    path('books/<int:pk>/get/', book_views.book.GetBookView.as_view(), name='book-get'),
    path('books/<int:pk>/return/', book_views.book.ReturnBookView.as_view(), name='book-return'),

    path('publishers/', book_views.publisher.PublisherListView.as_view(), name='publisher-list'),
    path('publishers/<int:pk>/', book_views.publisher.PublisherDetailView.as_view(), name='publisher-details'),

    path('users/readers/registration/', user_views.reader.ReaderCreateView.as_view(), name='reader-registration'),
    path('users/readers/login/', user_views.reader.ReaderLoginView.as_view(), name='reader-login'),
    path('users/readers/logout/', user_views.reader.ReaderLogoutView.as_view(), name='reader-logout'),
    path('users/readers/profile/', user_views.reader.ReaderProfileView.as_view(), name='reader-profile'),

    path('admin/', admin.site.urls),
]
