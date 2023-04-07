from random import random

from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from .forms import QuestionForm
from .models import Subject, Topic, Question, Quiz
from .serializers import QuestionSerializer, TopicSerializer, SubjectSerializer
########################## test area ######################################

def quiz_subject(request):
    if request.method == 'POST':
        # get list of selected subjects
        selected_subjects = request.POST.getlist('subject')

        # filter topics related to selected subjects
        topics = Topic.objects.filter(subject__in=selected_subjects)

        return render(request, 'quiz/ms_form2.html', {'topics': topics})

    # if request method is GET, show form to select subjects
    subjects = Subject.objects.all()
    return render(request, 'quiz/ms_form1.html', {'subjects': subjects})

# def quiz_topic(request):
#     if request.method == 'POST':
#         # get selected topics and mcq numbers
#         selected_topics = request.POST.getlist('topic')
#
#         # retrieve questions for selected topics and mcq numbers
#         questions = []
#         for i in range(len(selected_topics)):
#             topic_id = selected_topics[i]
#             topic_questions = Question.objects.filter(topic=topic_id)
#             questions.extend(list(topic_questions))
#
#         # create hidden_q string
#         hidden_q = ''
#         for q in questions:
#             hidden_q += str(q.id) + '#'
#
#         return render(request, 'quiz/test1.html', {'questions': questions, 'hidden_q': hidden_q})
#
#     # if request method is GET, redirect to multi_topic view
#     return redirect('multi_topic')


def generate_quiz(request):
    # Step 1: Get all the available subjects
    subjects = Subject.objects.all()

    # Step 2: If a subject has been selected, get its related topics
    selected_subject = request.GET.get('subject')
    if selected_subject:
        selected_subject = int(selected_subject)
        topics = Topic.objects.filter(subject=selected_subject)
    else:
        topics = []

    # Step 3: If topics have been selected, get their related questions
    selected_topics = request.GET.getlist('topics')
    if selected_topics:
        selected_topics = [int(topic) for topic in selected_topics]
        questions = Question.objects.filter(topic__in=selected_topics)
    else:
        questions = []

    # Step 4: If the form has been submitted, create a new quiz
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        selected_questions = request.POST.getlist('questions')

        quiz = Quiz.objects.create(name=name, description=description)
        quiz.subjects.add(selected_subject)
        quiz.topics.add(*selected_topics)
        quiz.questions.add(*selected_questions)

        return redirect('topic_list')

    context = {
        'subjects': subjects,
        'selected_subject': selected_subject,
        'topics': topics,
        'selected_topics': selected_topics,
        'questions': questions,
    }
    return render(request, 'quiz/create_quiz.html', context)


########################## test area #################################
def single_topic(request):
    if request.method == 'GET':
        subjects = Subject.objects.all()
        topics = Topic.objects.all()
        return render(request, 'quiz/stp_form.html', {'subjects':subjects,'topics':topics})

    if request.method == 'POST':
        subject_id = request.POST.get("subject", "")
        topic_id = request.POST.get("topic", "")
        mcq_no = request.POST.get("mcq_no", "")
        print(subject_id, topic_id, mcq_no)

        subjects = Subject.objects.all
        if subject_id != '':
            if topic_id != '':
                if int(mcq_no) >= 0 and int(mcq_no) <150:
                    return HttpResponseRedirect(reverse('test', kwargs={'subject':subject_id, 'topic':topic_id, 'mcq_no': mcq_no }))
                else:
                    pass
            else :
                topics = Subject.objects.get(id=subject_id).topic_set.all()
        else:
            topics = Topic.objects.all()
        subject_id = int(subject_id)
        return render(request, 'quiz/stp_form.html', {'subjects':subjects,'topics':topics, 'current_subject_id':subject_id})

def multi_topic(request):
    if request.method == 'POST':
        # get list of selected subjects
        selected_subjects = request.POST.getlist('subject')

        # filter topics related to selected subjects
        topics = Topic.objects.filter(subject__in=selected_subjects)

        return render(request, 'quiz/mtp_form2.html', {'topics': topics})

    # if request method is GET, show form to select subjects
    subjects = Subject.objects.all()
    return render(request, 'quiz/mtp_form1.html', {'subjects': subjects})


def multi_topic_test(request):
    if request.method == 'POST':
        # get selected topics and mcq numbers
        selected_topics = request.POST.getlist('topic')
        mcq_numbers = request.POST.getlist('mcq_no')

        # retrieve questions for selected topics and mcq numbers
        questions = []
        for i in range(len(selected_topics)):
            topic_id = selected_topics[i]
            mcq_no = int(mcq_numbers[i])
            topic_questions = Question.objects.filter(topic=topic_id)[:mcq_no]
            questions.extend(list(topic_questions))

        # create hidden_q string
        hidden_q = ''
        for q in questions:
            hidden_q += str(q.id) + '#'

        return render(request, 'quiz/test1.html', {'questions': questions, 'hidden_q': hidden_q})

    # if request method is GET, redirect to multi_topic view
    return redirect('multi_topic')


def test(request, subject, topic, mcq_no):
    # if request.method == "GET":
    s = Subject.objects.get(id=subject)
    t = Topic.objects.get(id=topic)
    selected_questions = Question.objects.filter(subject=s, topic=t)[:mcq_no]
    hidden_q =  ''
    for q in selected_questions:
        hidden_q += str(q.id)+'#'
    return render(request, 'quiz/test1.html', {'questions':selected_questions, 'hidden_q': hidden_q})

def result_view(request):
    if request.method == 'POST':
        attempted = {}
        hidden_q = request.POST.get("hidden_q", "")
        hidden_q = hidden_q.split('#')
        hidden_q = list(map(int, hidden_q[:-1]))
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken' and key!='hidden_q':
                attempted[key]=value

        q_list = Question.objects.filter(id__in=hidden_q)
        total_correct = 0
        total_attempted = len(attempted)

        for q_id in hidden_q:
            question = Question.objects.get(id=q_id)
            selected_option = attempted.get(str(q_id))
            if selected_option == question.correct_option:
                total_correct += 1

        context = {'questions': q_list, 'attempted': attempted, 'total_attempted': total_attempted, 'total_correct': total_correct}
        return render(request, 'quiz/result.html', context)

def load_questions(request):
    subject_id = request.POST.get('subject')
    topic_id = request.POST.get('topic')
    num_questions = request.POST.get('num_questions')
    questions = Question.objects.filter(subject_id=subject_id, topic_id=topic_id)[:num_questions]
    context = {'questions': questions}
    return render(request, 'quiz/questions.html', context)

################################ working code ##############

# Subject views
class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# Topic views
class TopicList(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


# Question views

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

@api_view(['GET', 'POST'])
def get_topics_view(request):
    subject_id = request.GET.get('subject_id')
    if subject_id:
        topics = Topic.objects.filter(subject_id=subject_id).values('id', 'topic')
        return JsonResponse(list(topics), safe=False)
    else:
        return JsonResponse([], safe=False)


@api_view(['GET', 'POST'])
def create_question(request):
    form = QuestionForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('question_list') # question list not created

    return render(request, 'quiz/question_form.html', {'form': form})

