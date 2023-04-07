from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from smart_selects.form_fields import ChainedManyToManyField


# Create your models here.

class Subject(models.Model):
    subject    = models.CharField(max_length=250,unique=True)
    def __str__(self):
        return "%s" % (self.subject)

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic  = models.CharField(max_length=100)


    def __str__(self):
        return "%s" % (self.topic)

class Question(models.Model):
    subject    = models.ForeignKey(Subject, on_delete=models.PROTECT)
    topic      = ChainedForeignKey(Topic, on_delete=models.PROTECT)
    question = models.TextField(max_length=700, null=False)
    option_A = models.CharField(max_length=150)
    option_B = models.CharField(max_length=150)
    option_C = models.CharField(max_length=150)
    option_D = models.CharField(max_length=150)
    correct_option = models.CharField(max_length=150)
    explaination = models.TextField(max_length=500, null=True ,blank=True)

    def save(self, *args, **kwargs):
        # Ensure only one correct option is selected
        correct_options = [o for o in [self.option_A, self.option_B, self.option_C, self.option_D] if
                           o == self.correct_option]
        if len(correct_options) != 1:
            raise ValueError('Exactly one option must be selected as correct')
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s %s %s" % (self.question[:100], self.topic, self.subject)


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True)
    subject = models.ManyToManyField(Subject, null=True, blank=True)
    topics = models.ManyToManyField(Topic, null=True,)
    questions = models.ManyToManyField(Question)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.questions.set(Question.objects.filter(topics__in=self.topics.all()))

    def __str__(self):
        return self.name