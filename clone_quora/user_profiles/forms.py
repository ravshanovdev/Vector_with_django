from django import forms
from django.utils.text import slugify

from .models import Profile


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # ...

    class Meta:
        model = Profile
        fields = ['username', 'profile_pic', 'biography', 'web_site_url', 'twitter_url', 'instagram_url',
                  'facebook_url', 'pinterest_url']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(),
            'biography': forms.Textarea(attrs={'class': 'form-control'}),
            'web_site_url': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
            'pinterest_url': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your username'})

        # Get the instance (if available) to access the current username value
        instance = kwargs.get('instance')
        if instance and instance.user:
            self.fields['username'].initial = instance.user.username
