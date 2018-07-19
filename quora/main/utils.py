from .models import *


def get_or_create_question(text,asked_by,asked_on):

    created = False

    try:
        text = text.strip()
        if not text.endswith('?'):
            text = text + '?'
        q = Question.objects.get(text=text)
    except Exception as e:
        q = Question.objects.create(text=text,
                                    asked_by=asked_by,
                                    asked_on=asked_on)
        created = True

    return q, created



def is_user_voted_question(question,user):

    qv = None
    created = False
    try:
        qv,created = QuestionVote.objects.get_or_create(question=question,user=user)
    except Exception as e:
        print(e.__str__())

    return qv,created



def is_user_voted_answer(answer,user):

    ansv = None
    created = False

    try:
        ansv,created = AnswerVote.objects.get_or_create(answer=answer,user=user)
    except Exception as e:
        print(e.__str__())

    return ansv,created