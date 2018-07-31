import os
import pytest
from django.utils import timezone
from datetime import datetime
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import *


"""Fixtures"""

pytestmark = pytest.mark.django_db

@pytest.fixture
@pytest.mark.django_db
def quser():
    user = User.objects.create(username='qtestuser',password='test12345')
    return user


@pytest.fixture
@pytest.mark.django_db
def auser():
    user =  User.objects.create(username='atestuser',password='test12345')
    return user


@pytest.fixture
@pytest.mark.django_db
def question(quser):
    qsn = Question.objects.create(text='random question?',
                                   asked_by=quser,
                                   asked_on=timezone.now())
    return qsn


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def answer(question,auser):
    ans =  Answer.objects.create(text='Answer',
                  question = question,
                  answered_by=auser,
                  answered_on=timezone.now())
    return ans



"""Test cases start here"""

def test_new_question_should_have_text(question):
    assert isinstance(question.text,str) == True

def test_new_question_should_have_valid_asked_by(question):
    assert isinstance(question.asked_by, User) == True


def test_new_question_should_have_zero_votes(question):
    assert 0 == question.votes


def test_new_question_should_have_valid_asked_on(question):
    assert isinstance(question.asked_on, datetime) == True


def test_answer_should_have_text(answer):
    assert isinstance(answer.text, str) == True

def test_answer_should_have_question(answer):
    assert isinstance(answer.question, Question) == True


def test_answer_should_have_answered_by(answer):
    assert isinstance(answer.answered_by, User) == True


def test_answer_should_have_valid_answered_on(answer):
    assert isinstance(answer.answered_on, datetime) == True


def test_answer_should_have_zero_votes(answer):
    assert 0 == answer.votes


def test_answer_should_have_valid_updated_on(answer):
    assert isinstance(answer.updated_on, datetime)


@pytest.mark.django_db
def test_answer_should_have_unique_question_and_answered_by(question,quser):

    ans1 = Answer.objects.create(
        text = 'Answer1',
        question = question,
        answered_by = quser,
        answered_on = timezone.now()
    )

    with pytest.raises(IntegrityError):
        Answer.objects.create(
            text = 'Answer2',
            question = question,
            answered_by = quser,
            answered_on = timezone.now()
        )



@pytest.mark.django_db
def test_multiple_answers_should_be_able_to_create_for_one_question(question,auser,quser):

    ans1 = Answer.objects.create(
        text = 'Answer1',
        question = question,
        answered_by = auser,
        answered_on = timezone.now()
    )

    ans2 = Answer.objects.create(
        text= 'Answer2',
        question = question,
        answered_by =  quser,
        answered_on = timezone.now()
    )
    assert ans1.question == question
    assert ans2.question == question


def test_upvote_question_should_increment_votes_count_by_one(question,auser):

    votes_before = question.votes
    question.increment_vote(auser)
    votes_after  = question.votes
    assert votes_after == votes_before + 1


@pytest.mark.django_db
def test_upvote_question_should_have_matching_QuestionVote_instance(question,auser):

    question.increment_vote(user=auser)
    qv = QuestionVote.objects.get(question=question,voted_by=auser)
    assert qv != None


def test_downvote_question_should_decrement_votes_count_by_one(question,auser):

    question.increment_vote(auser)
    votes_before = question.votes
    question.decrement_vote(auser)
    votes_after = question.votes
    assert votes_after == votes_before - 1


@pytest.mark.django_db
def test_downvote_question_should_delete_matching_QuestionVote_instance(question,auser):

    question.decrement_vote(auser)
    with pytest.raises(QuestionVote.DoesNotExist):
        QuestionVote.objects.get(question=question,voted_by=auser)


def test_upvote_question_should_allow_once_per_user(question,auser):

    votes_before = question.votes
    question.increment_vote(auser)
    question.increment_vote(auser)
    votes_after = question.votes
    assert votes_after == votes_before + 1


def test_downvote_question_should_allowe_once_per_user(question, auser):

    question.increment_vote(auser)
    votes_before = question.votes
    question.decrement_vote(auser)
    question.decrement_vote(auser)
    votes_after = question.votes
    assert votes_after == votes_before - 1


def test_upvote_answer_should_increment_votes_count_by_one(answer, quser):

    votes_before = answer.votes
    answer.increment_vote(quser)
    votes_after = answer.votes
    assert votes_after == votes_before + 1


@pytest.mark.django_db
def test_upvote_answer_should_have_matching_AnswerVote_instance(answer, quser):

    answer.increment_vote(quser)
    av = AnswerVote.objects.get(answer=answer,voted_by=quser)
    assert av != None


def test_downvote_answer_should_decrement_votes_count_by_one(answer, quser):

    answer.increment_vote(quser)
    votes_before = answer.votes
    answer.decrement_vote(quser)
    votes_after = answer.votes
    assert votes_after == votes_before - 1

@pytest.mark.django_db
def test_downvote_answer_should_have_matching_AnswerVote_instance(answer, quser):

    answer.decrement_vote(quser)
    with pytest.raises(AnswerVote.DoesNotExist):
        AnswerVote.objects.get(answer=answer, voted_by=quser)


def test_answer_upvote_multiple_times_should_not_increment_votes_count_more_than_one(answer, quser):

    votes_before = answer.votes
    answer.increment_vote(quser)
    answer.increment_vote(quser)
    votes_after = answer.votes
    assert votes_after == votes_before + 1



def test_answer_downvote_multiple_times_should_not_decrement_votes_count_more_than_one(answer, quser):

    answer.increment_vote(quser)
    votes_before = answer.votes
    answer.decrement_vote(quser)
    answer.decrement_vote(quser)
    votes_after = answer.votes
    assert  votes_after == votes_before - 1


