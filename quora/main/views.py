from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from allauth.account.decorators import login_required
from .models import Question,Answer,QuestionVote,AnswerVote
from .forms import QuestionForm,AnswerForm
from datetime import datetime
from .utils import (get_or_create_question,
                    is_user_voted_question,
                    is_user_voted_answer)

# Create your views here.
@login_required
def home(request):

    qa_details = []

    try:
        questions = Question.objects.all().order_by('-votes')
        for q in questions:
            answer = None
            answer_qset = q.answer_set.all().order_by('-votes')[:1]
            if answer_qset:
                answer = answer_qset.get()
            qa_details.append({'question':q,'answer':answer})
    except Exception as e:
        print(e.__str__())

    return render(request, 'main/home.html', context={'qa_pairs': qa_details})


@login_required
def ask_question(request):

    created = False
    form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('question')
            asked_on = datetime.now()
            q, created = get_or_create_question(text=text, asked_by=request.user, asked_on=asked_on)

    if created:
        return redirect(to='/')

    return render(request, 'main/ask_question.html', context={'form': form,'bounded':form.is_bound,'created': created})

@login_required
@require_http_methods('GET')
def question_detail(request):
    context = {}
    q = None
    try:
        qid = request.GET.get('qid')
        try:
            q = Question.objects.get(id=qid)
        except Exception as e:
            print(e.__str__())
            return redirect(to='/')
        answers = q.answer_set.all().order_by('-votes')
        context['question'] = q
        context['answers'] = answers
    except Exception as e:
        print(e.__str__())

    return render(request, 'main/question_detail.html', context=context)

@login_required
def post_answer(request):

    form = AnswerForm()
    question = None
    answered = False
    try:
        qid = request.GET.get('qid')
        try:
            question = Question.objects.get(id=qid)
        except Exception as e:
            print(e.__str__())
            question = None
        if question:
            try:
                user_ans = question.answer_set.get(answered_by=request.user)
            except Exception as e:
                user_ans = None
            if request.method == 'GET':
                if user_ans:
                    form = AnswerForm({'answer': user_ans.text})
            elif request.method == 'POST':
                form = AnswerForm(request.POST)
                if form.is_valid():
                    answer = form.cleaned_data.get('answer')
                    if answer:
                        if user_ans:
                            if user_ans.text.strip() != answer.strip():
                                user_ans.text = answer
                                user_ans.save()
                                answered = True
                            else:
                                answered = True
                        else:
                            answered_on = datetime.now()
                            ans = Answer.objects.create(text=answer,
                                                        question=question,
                                                        answered_by=request.user,
                                                        answered_on=answered_on)
                            answered = True

        else:
           return redirect(to='/')

    except Exception as e:
        print(e.__str__())
    if answered:
        return redirect(to='/')
    return render(request,'main/post_answer.html',{'form':form,'question':question})


@login_required
@require_http_methods('GET')
def upvote_question(request):

    redirect_to = None
    try:
        qid = request.GET.get('qid')
        redirect_to = request.GET.get('redirect_to')
        if not redirect_to:
            redirect_to = '/'
        if qid:
            q = Question.objects.get(id=qid)
            qv,created = QuestionVote.objects.get_or_create(question=q,voted_by=request.user)
            if created:
                q.votes += 1
                q.save()
    except Exception as e:
        print(e.__str__())

    return redirect(to=redirect_to)


@login_required
@require_http_methods('GET')
def downvote_question(request):

    redirect_to = None
    try:
        qid = request.GET.get('qid')
        redirect_to = request.GET.get('redirect_to')
        if not redirect_to:
            redirect_to = '/'
        q = Question.objects.get(id=qid)
        try:
           qv = QuestionVote.objects.get(question=q,voted_by=request.user)
        except Exception as e:
            qv = None
        if qv:
            if q.votes > 0:
                q.votes -= 1
                qv.delete()
                q.save()
    except Exception as e:
        pass
    return redirect(to=redirect_to)


@login_required
@require_http_methods('GET')
def upvote_answer(request):

    redirect_to = None
    try:
        answerid = request.GET.get('answerid')
        redirect_to = request.GET.get('redirect_to')
        if not redirect_to:
            redirect_to = '/'
        answer = Answer.objects.get(id=answerid)
        ansv,created = AnswerVote.objects.get_or_create(answer=answer,voted_by=request.user)
        if created:
            answer.votes += 1
            answer.save()
    except Exception as e:
        pass

    return redirect(to=redirect_to)


@login_required
@require_http_methods('GET')
def downvote_answer(request):

    redirect_to = None
    try:
        answerid = request.GET.get('answerid')
        redirect_to = request.GET.get('redirect_to')
        if not redirect_to:
            redirect_to = '/'
        answer = Answer.objects.get(id=answerid)
        try:
            ansv = AnswerVote.objects.get(answer=answer,voted_by=request.user)
        except Exception as e:
            ansv = None
        if ansv:
            if answer.votes > 0:
                ansv.delete()
                answer.votes -= 1
                answer.save()
    except Exception as e:
        pass

    return redirect(to=redirect_to)











