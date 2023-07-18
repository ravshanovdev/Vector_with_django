from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Category, Post, Answer, Question, Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.http import JsonResponse, Http404
from .forms import QuestionForm, AnswerForm, CommentForm, CreatePostForm
from django.db.models import Q


# postlar uchun view lar
def LikeView(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_slug'))
    post.likes.add(request.user.id)
    return HttpResponseRedirect(reverse('post_detail', args=[str(slug)]))


@login_required(login_url='login')
def blog_post_view(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CreatePostForm()

    if 'q' in request.GET:
        q = request.GET['q']
        blog = Post.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
    else:
        q = None
        blog = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('questions_list')
    else:
        question_form = QuestionForm()

    return render(request, 'home.html', {'post_list': blog, 'q': q, 'form': form, 'question_form': question_form})


# class BlogPostView(ListView):
#     model = Post
#     template_name = 'home.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.order_by('created_at')  # Tartibni o'zgartirish
        context['comments'] = comments
        total_likes = post.total_likes()  # total_likes() metodi orqali total_likes ni olish
        context['total_likes'] = total_likes
        return context


# def CreatePostView(request):
#     if request.method == 'POST':
#         form = CreatePostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CreatePostForm()
#     return render(request, 'post/create_post.html', {'form': form})
#


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
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


def QuestionListView(request):
    if 'q' in request.GET:
        q = request.GET['q']
        question = Question.objects.filter(Q(body_question__icontains=q))
    else:
        q = None
        question = Question.objects.all().order_by('-created_at')

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('questions_list')
    else:
        question_form = QuestionForm()

    if request.method == 'POST':
        post_form = CreatePostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        post_form = CreatePostForm()

    return render(request, 'question/questions_list.html', {'questions': question, 'q': q,
                                                            'question_form': question_form,
                                                            'post_form': post_form})


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
    model = Answer
    form_class = AnswerForm
    template_name = 'answer/create_answer.html'

    def form_valid(self, form):
        question_id = self.kwargs['question_id']
        question = Question.objects.get(id=question_id)
        answer = form.save(commit=False)
        answer.user = self.request.user
        answer.question = question
        answer.save()
        return super().form_valid(form)

    def get_success_url(self):
        question_id = self.kwargs['question_id']
        return reverse('question_detail', args=[question_id])


class AnswerDetailView(DetailView):
    model = Answer
    template_name = 'detail_answer.html'


def answer_list(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question_id=question_id)
    return render(request, 'answer/answer_list.html', {'question': question, 'answers': answers})


# comment uchun


# def add_comment(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)
#     if request.method == 'POST':
#         body = request.POST.get('body')
#         if body:
#             comment = Comment.objects.create(
#
#                 name=request.user,
#                 body=body
#             )
#             return redirect('post_detail', slug=post_slug)
#     return render(request, 'add_comment.html', {'post': post})


class CreateCommentView(CreateView):
    model = Comment
    template_name = 'comment/add_comment.html'
    fields = ['body']

    def form_valid(self, form):
        post_slug = self.kwargs['post_slug']
        post = get_object_or_404(Post, slug=post_slug)
        form.instance.post = post
        form.instance.name = self.request.user
        form.instance.created_at = timezone.now()  # Qo'shilgan vaqtini belgilash
        return super().form_valid(form)

    def get_success_url(self):
        post_slug = self.kwargs['post_slug']
        return reverse_lazy('post_detail', kwargs={'slug': post_slug})

