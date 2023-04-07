from django.contrib import admin
from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter

from . import models
from .models import Subject,Topic,Question, Quiz

# Register your models here.
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    list_filter = (
        ('subject', MultiSelectFieldListFilter),
        ('topics', MultiSelectFieldListFilter),
    )

admin.site.register(Quiz, QuizAdmin)
# class SubjectTopicFilter(admin.SimpleListFilter):
#     title = 'Subject and Topic'
#     parameter_name = 'subject_topic'
#
#     def lookups(self, request, model_admin):
#         subjects = set()
#         topics = set()
#         for quiz in model_admin.model.objects.all():
#             for subject in quiz.subject.all():
#                 subjects.add((subject.id, subject.name))
#                 for topic in quiz.topics.filter(subject=subject):
#                     topics.add((topic.id, f'{subject.name} - {topic.name}'))
#         subject_choices = sorted(list(subjects), key=lambda x: x[1])
#         topic_choices = sorted(list(topics), key=lambda x: x[1])
#         choices = []
#         choices.append(('subjects', subject_choices))
#         choices.append(('topics', topic_choices))
#         return choices
#
#     def queryset(self, request, queryset):
#         if self.value() == 'subjects':
#             subject_ids = request.GET.getlist('subject_topic')
#             topic_ids = Topic.objects.filter(subject__in=subject_ids).values_list('id', flat=True)
#             question_ids = Question.objects.filter(topics__in=topic_ids).values_list('id', flat=True)
#             return queryset.filter(questions__in=question_ids).distinct()
#         elif self.value() == 'topics':
#             topic_ids = request.GET.getlist('subject_topic')
#             question_ids = Question.objects.filter(topics__in=topic_ids).values_list('id', flat=True)
#             return queryset.filter(questions__in=question_ids).distinct()
#         else:
#             return queryset
#
#     def choices(self, changelist):
#         # Override the default behavior of the choices() method to filter the available topics and questions based on the selected subjects.
#         choices = super().choices(changelist)
#         selected_subject_ids = changelist.get_filters_params().get('subject_topic')
#         if selected_subject_ids:
#             selected_subject_ids = selected_subject_ids.split(',')
#             selected_topic_ids = Topic.objects.filter(subject__id__in=selected_subject_ids).values_list('id', flat=True)
#             available_topics = set(
#                 Question.objects.filter(topics__in=selected_topic_ids).values_list('topics__id', flat=True))
#             choices = [choice for choice in choices if
#                        str(choice['value']).isdigit() and int(choice['value']) in available_topics]
#             available_questions = set(
#                 Question.objects.filter(topics__in=selected_topic_ids).values_list('id', flat=True))
#             for choice in choices:
#                 if str(choice['value']).isdigit():
#                     topic_id = int(choice['value'])
#                     choice['subset'] = [question for question in choice['subset'] if
#                                         question['value'] in available_questions and topic_id in Question.objects.get(
#                                             id=question['value']).topics.all().values_list('id', flat=True)]
#         return choices
#
#
# class QuizAdmin(admin.ModelAdmin):
#     list_display = ['name', 'description']
#     list_filter = [SubjectTopicFilter]
#     filter_horizontal = ['subject', 'topics', 'questions']
#
# admin.site.register(Quiz, QuizAdmin)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Question)