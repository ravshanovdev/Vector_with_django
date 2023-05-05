from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Category, Post, Answer, Question, Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from django.http import JsonResponse, Http404
from .forms import QuestionForm, AnswerForm


# postlar uchun view lar
def LikeView(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_slug'))
    post.likes.add(request.user.id)
    return HttpResponseRedirect(reverse('post_detail', args=[str(slug)]))


class BlogPostView(ListView):
    model = Post
    template_name = 'post/post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        stuff = get_object_or_404(Post, slug=self.kwargs['slug'])
        total_likes = stuff.total_likes()
        context['total_likes'] = total_likes
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post/create_post.html'
    fields = ['title', 'description', 'photo']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post/update_post.html'
    fields = ['title', 'description', 'photo']

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post/delete_post.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


# savollar uchun view lar
class QuestionListView(ListView):
    model = Question
    template_name = 'question/questions_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.get_queryset()
        return context


class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'question/create_question.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DetailQuestionView(DetailView):
    model = Question
    template_name = 'question/question_detail.html'


class DeleteQuestionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = 'question/delete_question.html'
    success_url = reverse_lazy('questions_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class UpdateQuestionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    template_name = 'question/update_question.html'
    form_class = QuestionForm

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Answer modeli uchun
class CreateAnswer(LoginRequiredMixin, CreateView):
    def get(self, request, question_id):
        question = Question.objects.get(id=question_id)
        form = AnswerForm()
        return render(request, 'answer/create_answer.html', {'form': form})

    def post(self, request, question_id):
        question = Question.objects.get(id=question_id)
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=question_id)
        return render(request, 'answer/create_answer.html', {'form': form})


class AnswerDetailView(DetailView):
    model = Answer
    template_name = 'detail_answer.html'


def answer_list(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question_id=question_id)
    return render(request, 'answer/answer_list.html', {'question': question, 'answers': answers})


# comment uchun
class CreateCommentView(CreateView):
    model = Comment
    template_name = 'comment/add_comment.html'
    fields = ['body']

    def form_valid(self, form):
        post_slug = self.kwargs['slug']
        post = get_object_or_404(Post, slug=post_slug)
        form.instance.post = post
        form.instance.name = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        post_slug = self.kwargs['slug']
        return reverse_lazy('post_detail', kwargs={'slug': post_slug})
