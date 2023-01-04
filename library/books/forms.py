from django import forms


class GetBookForm(forms.Form):
    when_date = forms.DateField(
        label="Date",
    )


class ReturnBookForm(forms.Form):
    return_date = forms.DateField(
        label="Date of return",
    )
