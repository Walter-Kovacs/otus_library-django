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

from books import views

urlpatterns = [
    path('', views.welcome, name='welcome'),

    path('genre/', views.genre.GenreListView.as_view(), name='genre-list'),
    path('genre/<int:pk>/', views.genre.GenreDetailView.as_view(), name='genre-details'),

    path('work/', views.work.WrittenWorkListView.as_view(), name='work-list'),
    path('work/<int:pk>/', views.work.WrittenWorkDetailView.as_view(), name='work-details'),

    path('author/', views.author.AuthorListView.as_view(), name='author-list'),
    path('author/<int:pk>', views.author.AuthorDetailView.as_view(), name='author-details'),

    path('admin/', admin.site.urls),
]
