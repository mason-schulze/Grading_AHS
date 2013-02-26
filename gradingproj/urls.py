from django.conf.urls import patterns, include, url
from user_manage.views import editInfo

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
    url(r'^login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete', {"render_failure": editInfo}, name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^account/info/edit', 'user_manage.views.editInfo'),
    url(r'^lesson/add', 'stu_response.views.createLesson'),
    url(r'^lesson/delete/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.deleteLesson'),
    url(r'^lesson/edit/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.editLesson'),
    url(r'^lesson/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.viewLesson'),
    url(r'^responses/(?P<lesson_id>[0-9a-zA-Z]+)/(?P<q_num>\d+)/$', 'stu_response.views.viewResponses'),
    url(r'^responses/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.viewResponses'),
    url(r'^responses/(?P<lesson_id>[0-9a-zA-Z]+)/u/(?P<stu_id>\d+)/$', 'stu_response.views.viewResponses'),
    url(r'^class/add/$', 'stu_response.views.createClass'),
    url(r'^class/(?P<class_id>[0-9a-zA-Z]+)/$', 'stu_response.views.viewClass'),
    url(r'^class/delete/(?P<class_id>[0-9a-zA-Z]+)/$', 'stu_response.views.deleteClass'),
    url(r'^class/removeself/(?P<class_id>[0-9a-zA-Z]+)/$', 'stu_response.views.removeSelfFromClass'),
    url(r'^account/classes/$', 'stu_response.views.listClasses'),
    url(r'^class/edit/(?P<class_id>[0-9a-zA-Z]+)/$', 'stu_response.views.editClass'),
    url(r'^home/$', 'stu_response.views.home'),
    url(r'^$', 'stu_response.views.home'),
    url(r'^ajax/setseen/(?P<r_id>\d+)/$', 'stu_response.views.toggleSeen'),
    url(r'^ajax/responses/(?P<lesson_id>[0-9a-zA-Z]+)/(?P<q_num>\d+)/$', 'stu_response.views.getResponses'),
    url(r'^ajax/responses/(?P<lesson_id>[0-9a-zA-Z]+)/$', 'stu_response.views.getResponses'),
    url(r'^ajax/responses/(?P<lesson_id>[0-9a-zA-Z]+)/u/(?P<stu_id>\d+)/$', 'stu_response.views.getResponses'),
    url(r'^ajax/lesson/(?P<lesson_id>[0-9a-zA-Z]+)/students/$', 'stu_response.views.getStudentsInLesson'),

)
