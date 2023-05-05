from django import forms
from .models import Question, Answer, Comment


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
