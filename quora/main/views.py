from django.shortcuts import render,redirect
from django.db import IntegrityError
from django.db.models import Prefetch
from django.views.decorators.http import require_http_methods
from allauth.account.decorators import login_required
from .models import Question,Answer,QuestionVote,AnswerVote
from .forms import QuestionForm,AnswerForm
from datetime import datetime
from .utils import get_or_create_question

# Create your views here.
@login_required
def home(request):

    qa_pairs = []
    questions = None
    try:
        questions = Question.objects.prefetch_related(Prefetch('answer_set')).order_by('-votes')
        for q in questions:
            answer = None
            try:
                answer = q.answer_set.latest('votes')
            except Answer.DoesNotExist as e:
                print(e.__str__())
            qa_pairs.append({'question': q, 'answer': answer})
    except Exception as e:
        print(e.__str__())

    return render(request, 'main/home.html', context={'qa_pairs': qa_pairs})


@login_required
def ask_question(request):

    created = False
    form = QuestionForm()
    try:
        if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('question')
                asked_on = datetime.now()
                q, created = get_or_create_question(text=text, asked_by=request.user, asked_on=asked_on)
                if created:
                    return redirect(to='/')
    except Exception as e:
        print(e.__str__())


    return render(request, 'main/ask_question.html', context={'form': form,'bounded':form.is_bound,'created': created})

@login_required
@require_http_methods('GET')
def question_detail(request, qid=None):
    context = {}
    try:
        q = Question.objects.get(id=qid)
        answers = q.answer_set.all().order_by('-votes')
        context['question'] = q
        context['answers'] = answers
    except Question.DoesNotExist as e:
        print(e.__str__())
        return redirect(to='/')

    return render(request, 'main/question_detail.html', context=context)


@login_required
def post_answer(request, qid=None):

    form = AnswerForm()
    question = None
    answered = False
    user_ans = None
    error = None

    try:
        question = Question.objects.get(id=qid)
        try:
            user_ans = question.answer_set.get(answered_by=request.user)
        except Answer.DoesNotExist as e:
            print(e.__str__())
    except Question.DoesNotExist as e:
        print(e.__str__())
        return redirect(to='/')

    if request.method == 'GET':
        if user_ans:
            form = AnswerForm({'answer': user_ans.text})

    elif request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data.get('answer')
            if user_ans:
                if user_ans.text.strip() != answer.strip():
                    user_ans.text = answer
                    user_ans.save()
                    answered = True
                else:
                    error = 'Answer is same as previous, not updated'
            else:
                answered_on = datetime.now()
                try:
                    ans = Answer.objects.create(text=answer,
                                            question=question,
                                            answered_by=request.user,
                                            answered_on=answered_on)
                    answered = True
                except IntegrityError as e:
                    print(e.__str__())
                    error = "Error occured while posting the answer."
    if answered:
        return redirect(to='/')
    return render(request,'main/post_answer.html',{'form':form,'bounded':form.is_bound,'question':question,'error':error})


@login_required
@require_http_methods('GET')
def upvote_question(request, qid=None):

    redirect_to = request.GET.get('redirect_to')
    if not redirect_to:
        redirect_to = '/'

    try:
        q = Question.objects.get(id=qid)
        qv,created = QuestionVote.objects.get_or_create(question=q,voted_by=request.user)
        if created:
            q.vote_increment()
    except Question.DoesNotExist as e:
        print(e.__str__())

    return redirect(to=redirect_to)


@login_required
@require_http_methods('GET')
def downvote_question(request, qid=None):

    redirect_to = request.GET.get('redirect_to')
    if not redirect_to:
        redirect_to = '/'

    try:
        q = Question.objects.get(id=qid)
        qv = QuestionVote.objects.get(question=q,voted_by=request.user)
        if q.votes > 0:
            q.vote_decrement()
            qv.delete()
    except Question.DoesNotExist as e:
        print(e.__str__())
    except QuestionVote.DoesNotExist as e:
        print(e.__str__())

    return redirect(to=redirect_to)


@login_required
@require_http_methods('GET')
def upvote_answer(request,answerid=None):

    redirect_to = request.GET.get('redirect_to')
    if not redirect_to:
        redirect_to = '/'
    try:
        answer = Answer.objects.get(id=answerid)
        ansv, created = AnswerVote.objects.get_or_create(answer=answer, voted_by=request.user)
        if created:
            answer.vote_increment()
    except Answer.DoesNotExist as e:
        print(e.__str__())

    return redirect(to=redirect_to)


@login_required
@require_http_methods('GET')
def downvote_answer(request,answerid=None):

    redirect_to = request.GET.get('redirect_to')
    if not redirect_to:
        redirect_to = '/'
    try:
        answer = Answer.objects.get(id=answerid)
        ansv = AnswerVote.objects.get(answer=answer,voted_by=request.user)
        if answer.votes > 0:
            ansv.delete()
            answer.vote_decrement()
    except Answer.DoesNotExist as e:
        print(e.__str__())
    except AnswerVote.DoesNotExist as e:
        print(e.__str__())

    return redirect(to=redirect_to)











