from django import forms
from .models import Question, Answer, Comment, Post


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Post's title"}))
    description = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'post body...'}))
    photo = forms.FileField(label='Photo', widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'description', 'photo', ]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['body_question', 'poster']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(QuestionForm, self).__init__(*args, **kwargs)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', 'poster']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AnswerForm, self).__init__(*args, **kwargs)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }
