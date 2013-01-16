# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
from stu_response.models import Lesson, Question, Response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import simplejson
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.template import RequestContext


@user_passes_test(lambda u: u.is_staff)
def createLesson(request):
    if(request.method == "POST"):
        questions = simplejson.loads(request.POST['questions'])
        lesson = Lesson(name=request.POST['lesson_name'], creator=User.objects.get(pk=request.user.id))
        lesson.save()
        for q in questions:
            if q['id'] == "":
                x = Question(text=q['q_text'], q_num=q['q_num'])
                x.save()
                lesson.questions.add(x)
            else:
                x = Question.objects.get(pk=q['id'])
                x.text = q['q_text']
                x.q_num = q['q_num']
                x.save()
        return redirect('/')
    else:
        try:
            num = int(request.GET['num']) + 1
        except KeyError:
            num = 1
        return render_to_response("stu_response/lesson_form.html", {"num": range(1, num)}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def editLesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, key=lesson_id)
    if request.user != lesson.creator:
        return HttpResponseForbidden("You do not have access to this page.")
    if(request.method == "POST"):
        questions = simplejson.loads(request.POST['questions'])
        lesson.name = request.POST['lesson_name']
        lesson.save()
        addedQ = []
        for q in questions:
            if q['id'] == "":
                x = Question(text=q['q_text'], q_num=q['q_num'])
                x.save()
                lesson.questions.add(x)
            else:
                x = Question.objects.get(pk=q['id'])
                x.text = q['q_text']
                x.q_num = int(q['q_num'])
                x.save()
            addedQ.append(x)
        q_set = lesson.questions.all()
        for x in q_set:
            for q in range(len(addedQ)):
                if x.id.__str__() == addedQ[q].id.__str__():
                    break
                elif q == len(questions) - 1:
                    x.delete()
                    break
        return redirect('/')
    return render_to_response("stu_response/lesson_form.html", {"questions": lesson.questions.all().order_by("q_num"), "lesson": lesson}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def deleteLesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, key=lesson_id)
    if lesson.creator == request.user:
        for r in lesson.recorded_responses.all():
            r.delete()
        for q in lesson.questions.all():
            q.delete()
        lesson.delete()
        return HttpResponse(simplejson.dumps({"success": True}), mimetype="application/json")
    else:
        return HttpResponseForbidden(simplejson.dumps({"success": False}), mimetype="application/json")


@login_required
def viewLesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, key=lesson_id)
    responses = []
    if lesson.recorded_responses.filter(student=User.objects.get(pk=request.user.id)):
        for q in lesson.questions.all().order_by("q_num"):
            try:
                r = Response.objects.get(question=q, student=User.objects.get(pk=request.user.id))
            except ObjectDoesNotExist:
                r = Response(student=User.objects.get(pk=request.user.id), text="", question=q)
                r.save()
            except MultipleObjectsReturned:
                temp = Response.objects.filter(question=q, student=User.objects.get(pk=request.user.id)).order_by("edit_date")
                for x in temp:
                    if x != temp[temp.count() - 1]:
                        x.delete()
                    else:
                        r = x
            curr = {
                "user_id": r.student.__str__(),
                "response": r.text,
                "last_edit": r.edit_date.__str__(),
                "q_num": r.question.q_num.__str__(),
            }
            responses.append(curr)
    if request.method == "POST":
        responses = simplejson.loads(request.POST['responses'])
        for r in responses:
            changed = False
            if Response.objects.filter(student=User.objects.get(pk=request.user.id), question=Question.objects.get(pk=r['id'])).count() > 0:
                response = Response.objects.get(student=User.objects.get(pk=request.user.id), question=Question.objects.get(pk=r['id']))
                if response.text != r['response']:
                    response.viewed = False
                    response.text = r['response']
                    changed = True
            else:
                response = Response(text=r['response'], student=User.objects.get(pk=request.user.id), question=Question.objects.get(pk=r['id']))
                changed = True
            if changed:
                response.save()
                lesson.recorded_responses.add(response)
        if request.is_ajax():
            return HttpResponse(simplejson.dumps({"success": True}), mimetype='application/json')
        return redirect('/')
    return render_to_response("stu_response/lesson_view.html", {"lesson": lesson, "questions": lesson.questions.all().order_by('q_num'), "responses": simplejson.dumps(responses)}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def viewResponses(request, lesson_id, q_num=None, stu_id=None):
    lesson = get_object_or_404(Lesson, key=lesson_id)
    if request.user != lesson.creator:
        return HttpResponseForbidden("You do not have access to this page.")
    lesson_set = lesson.questions.all().order_by('q_num')
    curr_q = None
    if q_num:
        curr_q = lesson.questions.get(q_num=q_num)
    return render_to_response("stu_response/response_view.html", {"questions": lesson_set, "lesson_key": lesson_id, "question": curr_q, "lesson": lesson, "lesson_id": lesson.id, "select_r": range(1, lesson.questions.count() + 1)}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def getResponses(request, lesson_id, q_num=None, stu_id=None):
    lesson = get_object_or_404(Lesson, key=lesson_id)
    if request.user != lesson.creator:
        return HttpResponseForbidden("You do not have access to this page.")
    lesson_set = lesson.questions.all().order_by('q_num')
    responses = []
    if q_num:
        responses.append(Response.objects.filter(question=lesson.questions.filter(q_num=q_num)).order_by("-edit_date"))
    elif stu_id:
        for question in lesson_set:
            responses.append(Response.objects.filter(question=question, student=User.objects.get(pk=stu_id)))
    else:
        for question in lesson_set:
            responses.append(Response.objects.filter(question=question).order_by("edit_date"))
    response_set = []
    for x in responses:
        for r in x:
            curr = {
                "response": r.text,
                "edit_date": r.get_format_date(),
                "viewed": r.viewed,
                "student": r.student.get_full_name(),
                "q_num": r.question.q_num,
                "r_id": r.id,
            }
            response_set.append(curr)
    return HttpResponse(simplejson.dumps({"responses": response_set}), mimetype="application/json")


@user_passes_test(lambda u: u.is_staff)
def getStudentsInLesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.user != lesson.creator:
        return HttpResponseForbidden("You do not have access to this page.")
    sample_q = lesson.questions.all().order_by('q_num')[0]
    responses = Response.objects.filter(question=sample_q)
    users = []
    for r in responses:
        curr = {
                "user_id": r.student.id,
                "username": r.student.username,
                "first_name": r.student.first_name,
                "last_name": r.student.last_name,
                "full_name": r.student.get_full_name(),
            }
        users.append(curr)
    return HttpResponse(simplejson.dumps(users), mimetype='application/json')


@user_passes_test(lambda u: u.is_staff)
def toggleSeen(request, r_id):
    if request.is_ajax() and request.GET.get('seen', False) and request.user.is_staff:
        r = Response.objects.get(pk=r_id)
        if request.user != r.getLesson().creator:
            return HttpResponseForbidden("You do not have access to this page.")
        r.viewed = True if request.GET['seen'] == '1' else False
        r.save()
        return HttpResponse(simplejson.dumps({"seen": r.viewed}), mimetype="application/json")
    return HttpResponseForbidden("You do not have the correct permissions to view this page")


def home(request):
    lessons = []
    if request.user.is_authenticated():
        if request.user.is_staff:
            for x in Lesson.objects.filter(creator=request.user).order_by('-creation_date'):
                curr = {
                    "lesson": x,
                    "creator": x.creator,
                    "num_users": len(x.getStudentsResponded()),
                    "num_complete": len(x.getStudentsCompleted()),
                }
                lessons.append(curr)
            return render_to_response("staff_home.html", {"lessons": lessons}, context_instance=RequestContext(request))
        else:
            responses = Response.objects.filter(student=User.objects.get(pk=request.user.id)).order_by("edit_date")
            temp = []
            for r in responses:
                lesson = r.getLesson()
                if lesson not in temp:
                    temp.append(lesson)
                    curr = {
                        "lesson": lesson,
                        "creator": lesson.creator,
                        "completed": lesson.getNumCompleted(user_id=request.user.id),
                    }
                    lessons.append(curr)
        return render_to_response("user_home.html", {"lessons": lessons}, context_instance=RequestContext(request))
    return render_to_response("home.html", context_instance=RequestContext(request))
