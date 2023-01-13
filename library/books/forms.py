from django import forms

from .models import (
    Author,
    Genre,
    WrittenWork,
)


class GetBookForm(forms.Form):
    when_date = forms.DateField(
        label="Date",
    )


class ReturnBookForm(forms.Form):
    return_date = forms.DateField(
        label="Date of return",
    )


class WrittenWorkForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
    )

    class Meta:
        model = WrittenWork
        fields = (
            'title',
            'authors',
            'genre',
            'description',
        )

    @property
    def title(self):
        return self.data['title']

    @property
    def authors_ids(self) -> tuple:
        return tuple(map(int, self.data.getlist('authors')))

    @property
    def genre_object(self):
        return Genre.objects.get(id=self.data['genre'])

    @property
    def description(self):
        return self.data['description']
