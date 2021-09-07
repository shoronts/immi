from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        error_messages={'required': 'Search For Topics Required.'},
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search For Topics',
                'class': 'form-control me-2',
                'aria-label': "Search",
                'type': 'search'
                }
            )
        )
