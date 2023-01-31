from django import forms

from .models import (
    Author,
    BookCopy,
    WrittenWork,
)


class RequestBookForm(forms.Form):
    pass


class LendBookForm(forms.Form):
    inventory_number = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
    )

    @property
    def copy_id(self) -> int:
        return int(self.data['inventory_number'])


class ReturnBookForm(forms.Form):
    pass


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
    def authors_ids(self) -> tuple:
        return tuple(map(int, self.data.getlist('authors')))

    def save(self, commit=True):
        work = super().save(commit)
        work.author_set.add(*self.authors_ids)
        return work
