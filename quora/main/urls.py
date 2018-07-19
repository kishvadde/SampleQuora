from django.urls import path,include
from .views import *

urlpatterns = [
    path('', home),
    path('ask-question', ask_question),
    path('post-answer',post_answer),
    path('question-detail',question_detail),
    path('upvote-question', upvote_question),
    path('upvote-answer',upvote_answer),
    path('downvote-question',downvote_question),
    path('downvote-answer',downvote_answer),
]