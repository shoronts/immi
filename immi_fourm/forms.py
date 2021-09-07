from django import forms
from .models import ForumPost


class SinglePostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'post_description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'}),
            'post_description': forms.Textarea(attrs={'class': 'form-control form-control-add-question',
                                                      'placeholder': 'Post details', 'style': 'height:300px'}),
            }

        error_messages = {
            'title': {'required': "Title Required."},
            'post_description': {'required': "Descriptions Required."},
        }


class EditSinglePost(forms.Form):
    title = forms.CharField(
        error_messages={'required': 'Title Required.'},
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Post Title'
                }
            )
        )

    post_description = forms.CharField(
        error_messages={'required': 'Discription Required.'},
        widget=forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'style': 'height:300px'
                }
            )
        )


class SearchForm(forms.Form):
    search = forms.CharField(
        error_messages={'required': 'Topics Required.'},
        max_length=100,
        widget=forms.TextInput(
            attrs={
                    'placeholder': 'Search For Topics',
                    'class': 'form-control form-control-update'
                }
            )
        )
