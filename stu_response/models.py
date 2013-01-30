from django.db import models
from django.contrib.auth.models import User
from django import forms
import random
from hashlib import sha1
import datetime
from django.utils import timezone
from django.utils.timezone import utc


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
    edit_date = models.DateTimeField()
    viewed = models.BooleanField(default=False)

    def __unicode__(self):
        return "(" + self.student.username + ") " + self.text

    def save(self, set_date=None, *args, **kwargs):
        if set_date:
            self.edit_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        super(Response, self).save(*args, **kwargs)

    def getLesson(self):
        return self.question.lesson_set.all()[0]

    def is_blank(self):
        return self.text.strip() == ""

    def get_format_date(self):
        return timezone.make_naive(self.edit_date, timezone.get_current_timezone()).strftime("%b. %d, %Y, %I:%M %p")


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

    def getResponses(self, q_num=None, stu_id=None):
        lesson_responses = []
        if q_num:
            question = self.questions.get(q_num=q_num)
            return Response.objects.filter(question=question).exclude(text="").order_by("-edit_date")
        elif stu_id:
            student = User.objects.get(pk=stu_id)
            q_set = self.questions.all().order_by('q_num')
            for q in q_set:
                q_responses = Response.objects.filter(question=q, student=student)
                if len(q_responses) != 0:
                    lesson_responses.append(q_responses)
        else:
            q_set = self.questions.all().order_by('q_num')
            for q in q_set:
                q_responses = Response.objects.filter(question=q).exclude(text="").order_by("-edit_date")
                if len(q_responses) != 0:
                    lesson_responses.append(q_responses)
        return lesson_responses

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


def getPercentComplete(user, lesson):
    total = lesson.questions.count()
    completed = lesson.getNumCompleted(user_id=user.id)
    return completed * 1.0 / total

def getRespondedLessons(user):
    all_lessons = Lesson.objects.all().order_by('-creation_date')
    lessons = []
    for l in all_lessons:
        if user in l.getStudentsResponded():
            lessons.append(l)
    return lessons


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text',)


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ('text',)
