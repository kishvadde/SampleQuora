from django.urls import path,include
from .views import *

urlpatterns = [
    path('', home),
    path('ask-question', ask_question),
    path('post-answer/<int:qid>',post_answer),
    path('question-detail/<int:qid>',question_detail),
    path('upvote-question/<int:qid>', upvote_question),
    path('upvote-answer/<int:answerid>',upvote_answer),
    path('downvote-question/<int:qid>',downvote_question),
    path('downvote-answer/<int:answerid>',downvote_answer),
]