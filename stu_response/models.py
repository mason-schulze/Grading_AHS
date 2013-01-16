from django.db import models
from django.contrib.auth.models import User
from django import forms
import random
from hashlib import sha1


class Question(models.Model):
    text = models.CharField(max_length=2000)
    q_num = models.IntegerField()

    def __unicode__(self):
        return self.text


class Response(models.Model):
    question = models.ForeignKey(Question)
    student = models.ForeignKey(User)
    text = models.CharField(max_length=3000)
    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    viewed = models.BooleanField(default=False)

    def __unicode__(self):
        return "(" + self.student.username + ") " + self.text

    def getLesson(self):
        return self.question.lesson_set.all()[0]

    def is_blank(self):
        return self.text.strip() == ""

    def get_format_date(self):
        return self.edit_date.strftime("%b. %d, %Y, %I:%M %p")


class Lesson(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User)
    questions = models.ManyToManyField(Question, blank=True)
    recorded_responses = models.ManyToManyField(Response, blank=True)
    key = models.CharField(unique=True, max_length=200)

    def __unicode__(self):
        return self.name

    def getStudentsResponded(self):
        responses = self.recorded_responses.all()
        users = []
        for r in responses:
            if r.student not in users:
                users.append(r.student)
        return users

    def getStudentsCompleted(self):
        students = self.getStudentsResponded()
        studentsDone = []
        for s in students:
            numDone = self.getNumCompleted(s.id)
            if numDone == self.questions.count():
                studentsDone.append(s)
        return studentsDone

    def get_view_url(self):
        return "/lesson/" + self.key + "/"

    def get_edit_url(self):
        return "/lesson/edit/" + self.key + "/"

    def get_response_url(self):
        return "/responses/" + self.key + "/"

    def getNumCompleted(self, user_id):
        user = User.objects.get(pk=user_id)
        responses = self.recorded_responses.filter(student=user)
        completed = 0
        for r in responses:
            if not r.is_blank():
                completed += 1
        return completed

    def save(self, *args, **kwargs):
        if self.key == None or self.key == "":
            key = sha1(str(random.random())).hexdigest()
            while Lesson.objects.filter(key=key).count() > 0:
                key = sha1(str(random.random())).hexdigest()
            self.key = key
        super(Lesson, self).save(*args, **kwargs)


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text',)


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ('text',)
