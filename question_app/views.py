from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404, render_to_response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist

from question_app.models import *


# Create your views here.


@login_required(login_url='/login')
@method_decorator(csrf_exempt, name='dispatch')
def voteField(request, question_id):
    args = {}
    args['question'] = Question.objects.get(id=question_id)
    args['answer'] = Answer.objects.all().filter(question_id=question_id)
    args['username'] = auth.get_user(request)
    return render_to_response('vote.html', args)


@login_required(login_url='/login')
@method_decorator(csrf_exempt, name='dispatch')
def vote(request, question_id):
    cook = question_id + '_question_' + auth.get_user(request).get_username()
    question = []
    try:

        if cook not in request.COOKIES:
            p = get_object_or_404(Question, pk=question_id)

            for choice in request.POST.getlist('choice'):
                try:
                    selected = p.answer_set.get(pk=choice)
                except (KeyError, Answer.DoesNotExist):
                    return render(request, 'vote.html', {'poll': p, 'error': 'Не выбран ответ!!!'})
                else:
                    selected.votes += 1
                    selected.save()
                    VotesResult.objects.create(answer=selected, interview=p.interview, question=p,
                                               user=auth.get_user(request))
            question.append(p)

            args = {'answer': Answer.objects.filter(question_id=question_id), 'username': auth.get_user(request),
                    'questions': question}
            response = render_to_response('result.html', args)
            response.set_cookie(cook, 'tester')
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')


@login_required(login_url='/login')
@method_decorator(csrf_exempt, name='dispatch')
def votes(request):
    cook = request.POST.get('interview') + '_interview_' + auth.get_user(request).get_username()
    question = []
    if cook not in request.COOKIES:

        for choice in request.POST.getlist('choice'):
            selected = Answer.objects.get(id=choice)
            selected.votes += 1
            selected.save()
            VotesResult.objects.create(answer=selected, interview=selected.question.interview,
                                       question=selected.question, user=auth.get_user(request))
            if not selected.question in question:
                question.append(selected.question)

        args = {'answer': Answer.objects.filter(question__interview_id=request.POST.get('interview')),
                'username': auth.get_user(request), 'questions': question}
        response = render_to_response('result.html', args)
        response.set_cookie(cook, 'tester', 3600)

        return response

    return redirect('/testers')


@login_required(login_url='/login')
@method_decorator(csrf_exempt, name='dispatch')
def detail(request):
    args = {'questions': Question.objects.filter(interview=None), 'username': auth.get_user(request), 'title': "Вопросы"}

    return render_to_response("main.html", args)


@login_required(login_url='/login')
@method_decorator(csrf_exempt, name='dispatch')
def tester(request, interview_id):
    args = {}
    args['question'] = Question.objects.filter(interview=interview_id)
    args['answers'] = Answer.objects.filter(question__interview_id=interview_id)
    args['username'] = auth.get_user(request)
    args['interview'] = interview_id
    args['title'] = "Опрос '%s'" % Interview.objects.get(id=interview_id).interview

    return render_to_response("tester.html", args)


@login_required(login_url='/login')
@method_decorator(csrf_exempt, name='dispatch')
def testers(request):
    args = {'groups': Interview.objects.all(), 'username': auth.get_user(request)}
    args['title'] = "Опросы"

    return render_to_response("tester.html", args)


@login_required(login_url='/login')
@method_decorator(csrf_exempt, name='dispatch')
def resultsInterview(request):
    args = {}
    args['groups'] = VotesResult.objects.exclude(interview=None).filter(user=auth.get_user(request))
    args['username'] = auth.get_user(request)
    args['title'] = "Результаты опросов"
    return render_to_response("results.html", args)


@login_required(login_url='/login')
@method_decorator(csrf_exempt, name='dispatch')
def index(request):
    return render_to_response('index.html', {'username': auth.get_user(request)})
