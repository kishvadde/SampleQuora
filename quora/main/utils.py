from .models import *


def get_or_create_question(text,asked_by,asked_on):

    created = False

    try:
        text = text.strip()
        if not text.endswith('?'):
            text = text + '?'
        q = Question.objects.get(text=text)
    except Question.DoesNotExist as e:
        q = Question.objects.create(text=text,
                                    asked_by=asked_by,
                                    asked_on=asked_on)
        created = True

    return q, created