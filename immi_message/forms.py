from django import forms


class create_group(forms.Form):
    create_group = forms.CharField(
        error_messages = {'required' : 'Group Name Required.'},
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'placeholder' : 'Create Group',
                'class' : 'form-control py-2'
                }
            )
        )
