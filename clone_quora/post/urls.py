from django.http import request
from django.urls import path
from .views import (
    # POstga oid
    PostDetailView,
    blog_post_view,
    LikeView,

    UpdatePostView,
    DeletePostView,
    # obunaga oid

    # "question"ga oid qism
    QuestionListView,

    DetailQuestionView,
    DeleteQuestionView,
    UpdateQuestionView,

    CreateAnswer,
    answer_list,
    AnswerDetailView,
    CreateCommentView,


)

urlpatterns = [
    # postga oid

    path('', blog_post_view, name='home'),


    # questionga oid
    # path('ask_question/', create_question_view, name='create_question'),
    path('question/<int:pk>/', DetailQuestionView.as_view(), name='question_detail'),




    path('answer_list/<int:question_id>/', answer_list, name='answer_list'),


    # post
    # path('create_Post/', CreatePostView.as_view(), name='create_post'),
    path('<slug:post_slug>/comment/', CreateCommentView.as_view(), name='add_comment'),
    # question
    path('questions/', QuestionListView, name='questions_list'),

    # answerga oid
    path('answer/<int:question_id>/', CreateAnswer.as_view(), name='create_answer'),
    # postga oid


    # postga oid
    path('<slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<slug>/update_post/', UpdatePostView.as_view(), name='update_post'),
    path('<slug>/delete_post/', DeletePostView.as_view(), name='delete_post'),
    path('like/<slug>/', LikeView, name='like_post'),

    path('update_question/<int:pk>/', UpdateQuestionView.as_view(), name='update_question'),
    path('delete_question/<int:pk>/', DeleteQuestionView.as_view(), name='delete_question'),

    # postlarga taluqli urls



]

