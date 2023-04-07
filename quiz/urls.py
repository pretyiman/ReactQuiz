from django.urls import path, include
from rest_framework import routers

from . import views
from .views import create_question, get_topics_view

router = routers.DefaultRouter()

urlpatterns = [
    ################################ testing area #################################
    path('create_question_new/', views.create_question, name='create_question_new'),
    path('generate_quiz',views.generate_quiz, name='generate_quiz'),
    ################################ testing area #################################
    # Subject endpoints
    path('subjects/', views.SubjectList.as_view(), name='subject_list'),
    path('subjects/<int:pk>/', views.SubjectDetail.as_view(), name='subject_detail'),

    # Topic endpoints
    path('topics/', views.TopicList.as_view(), name='topic_list'),
    path('topics/<int:pk>/', views.TopicDetail.as_view(), name='topic_detail'),

    # Question endpoints
    path('questions/', views.QuestionList.as_view(), name='question_list'),
    path('questions/<int:pk>/', views.QuestionDetail.as_view(), name='question_detail'),

    # Custom endpoints
    path('single_topic', views.single_topic, name='single_topic'),
    path('test/<subject>/<topic>/<int:mcq_no>', views.test, name='test'),

    path('multi_topic/', views.multi_topic, name='multi_topic'),
    path('multi_topic_test/', views.multi_topic_test, name='multi_topic_test'),
    path('results',views.result_view, name='results'),
    # working urls
    path('get_topics/', views.get_topics_view, name='get_topics'),
    # path('create_question/', views.create_question, name='create_question'),

    # path('question/', create_question, name='question'),
    # path('get_topics/', get_topics_view, name='get_topics'),
    path('api/', include(router.urls)),
]
