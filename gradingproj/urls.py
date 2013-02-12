from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_change, logout_then_login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gradingproj.views.home', name='home'),
    # url(r'^gradingproj/', include('gradingproj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, {'template_name': 'usermanage/login.html'}),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^relog/$', logout_then_login),
    url(r'^account/editpassword/$', password_change, {'template_name': 'usermanage/user_form_base.html', 'post_change_redirect': '/relog/'}),
    url(r'^lesson/create', 'stu_response.views.createLesson'),
    url(r'^lesson/delete/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.deleteLesson'),
    url(r'^lesson/edit/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.editLesson'),
    url(r'^lesson/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.viewLesson'),
    url(r'^responses/(?P<lesson_id>[0-9a-zA-Z]+)/(?P<q_num>\d+)/$', 'stu_response.views.viewResponses'),
    url(r'^responses/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.viewResponses'),
    url(r'^responses/(?P<lesson_id>[0-9a-zA-Z]+)/u/(?P<stu_id>\d+)/$', 'stu_response.views.viewResponses'),
    url(r'^class/add/$', 'stu_response.views.createClass'),
    url(r'^account/classes/$', 'stu_response.views.viewClasses'),
    url(r'^class/edit/(?P<class_id>[0-9a-zA-Z]+)/$', 'stu_response.views.editClass'),
    url(r'^student/register/$', 'user_manage.views.registerStudent'),
    url(r'^teacher/register/$', 'user_manage.views.registerTeacher'),
    url(r'^getusers/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.getStudentsInLesson'),
    url(r'^home/$', 'stu_response.views.home'),
    url(r'^$', 'stu_response.views.home'),
    url(r'^ajax/login/$', 'user_manage.views.ajaxLogin'),
    url(r'^ajax/setseen/(?P<r_id>\d+)/$', 'stu_response.views.toggleSeen'),
    url(r'^ajax/responses/(?P<lesson_id>[0-9a-zA-Z]+)/(?P<q_num>\d+)/$', 'stu_response.views.getResponses'),
    url(r'^ajax/responses/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.getResponses'),
    url(r'^ajax/responses/(?P<lesson_id>[0-9a-zA-Z]+)/u/(?P<stu_id>\d+)/$', 'stu_response.views.getResponses'),
)
