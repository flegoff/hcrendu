from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hcrendu.views.home', name='home'),
    # url(r'^hcrendu/', include('hcrendu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'hcrendu.hcstudyprojects.views.projects', name="projects"),
    url(r'^project/(?P<project_id>\d+)$', 'hcrendu.hcstudyprojects.views.project', name="project"),
    url(r'^project/(?P<project_id>\d+)/register$', 'hcrendu.hcstudyprojects.views.request_access', name="project-register"),
    url(r'^access/(?P<key>\S+)$', 'hcrendu.hcstudyprojects.views.access_project', name="access-project"),
    url(r'^answer/(?P<question_id>\d+)$', 'hcrendu.hcstudyprojects.views.answer_question', name="answer"),
    url(r'^upload/(?P<question_id>\d+)$', 'hcrendu.hcstudyprojects.views.answer_question_with_file', name="upload-answer"),
    
)
