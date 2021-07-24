from django import forms
from .models import forum_post


class single_post_form(forms.ModelForm):
    class Meta:
        model = forum_post
        fields = ['title', 'post_discription', 'post_images']

        widgets = {
            'title' : forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'Post Title'}),
            'post_discription' : forms.Textarea(attrs = {'class':'form-control', 'placeholder': 'Post Details', 'style': 'height:300px'}),
            'post_images' : forms.FileInput(attrs={'class':'form-control'}),
            }

        error_messages = {
            'title' : {'required' : "Title Required."},
            'post_discription' : {'required' : "Descriptions Required."},
            'post_images' : {'required' : "Image Required."},
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

    post_images = forms.CharField(
        required=False,
        widget = forms.FileInput(
            attrs = {
                'class' : 'form-control'
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