from django import forms


class GetBookForm(forms.Form):
    when_date = forms.DateField(
        label="Date",
    )
