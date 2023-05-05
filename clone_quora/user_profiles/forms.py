from django import forms
from django.utils.text import slugify

from .models import Profile


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['username', 'profile_pic', 'biography', 'web_site_url', 'twitter_url', 'instagram_url',
                  'facebook_url',
                  'pinterest_url']

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
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'change your name'}),

        self.fields['profile_pic'].required = False  # <-- This line here to remove "required" attribute

        self.fields['biography'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tell us about yourself'})
        self.fields['web_site_url'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'do you have a web site?'})
        self.fields['twitter_url'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'do yoy have a twitter account?'})
        self.fields['instagram_url'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'do yoy have a instagram account?'})
        self.fields['facebook_url'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'do yoy have a facebook account?'})
        self.fields['pinterest_url'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'do yoy have a pinterest account?'})

    # def save(self, user, commit=True):
    #     profile = super(ProfileForm, self).save(commit=False)
    #     profile.user = user
    #     profile.slug = slugify(user.username)
    #     if commit:
    #         profile.save()
    #     return profile
