from django import forms
from .models import forum_post


class single_post_form(forms.ModelForm):
    class Meta:
        model = forum_post
        fields = ['title', 'post_discription']

        widgets = {
            'title' : forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'Post Title'}),
            'post_discription' : forms.Textarea(attrs = {'class':'form-control form-control-add-question', 'placeholder': 'Post Details', 'style': 'height:300px'}),
            }

        error_messages = {
            'title' : {'required' : "Title Required."},
            'post_discription' : {'required' : "Descriptions Required."},
        }

class edit_single_post(forms.Form):
    title = forms.CharField(
        error_messages = {'required' : 'Title Required.'},
        widget=forms.TextInput(
            attrs = {
                'class':'form-control',
                'placeholder': 'Post Title'
                }
            )
        )

    post_discription = forms.CharField(
        error_messages = {'required' : 'Discription Required.'},
        widget = forms.Textarea(
                attrs = {
                'class':'form-control',
                'style': 'height:300px'
                }
            )
        )

class search_form(forms.Form):
    search = forms.CharField(
        error_messages = {'required' : 'Topics Required.'},
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'placeholder' : 'Search For Topics',
                'class' : 'form-control form-control-update'
                }
            )
        )
