# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from hcrendu.hcstudyprojects.models import Project, ProjectQuestion, StudentFile, StudentFileForm, \
                                            StudentAnswer, StudentAnswerForm, AutoRegisteredStudent, \
                                            AutoRegisteredStudentForm

from datetime import datetime
import logging

def projects(request):
    now = datetime.now()
    logging.error("{0}".format(now))
    return render_to_response('hcstudyprojects/projects.html',
        { 'projects': Project.objects.filter(active=True) },
        context_instance=RequestContext(request))


def project(request, project_id):
    
    project = get_object_or_404(Project, pk=project_id)

    if not 'projects' in request.session or \
        not project.id in request.session['projects']:
        messages.error(request, "We were not able to authenticate you. Please re-connect.")
        return HttpResponseRedirect('/')
    
    if not project.is_upload_open():
        messages.error(request, "It's too late, submissions for this project are now closed.")
        return HttpResponseRedirect('/project/{0}'.format(project.id))

    return render_to_response('hcstudyprojects/project.html',
        { 'project': project },
        context_instance=RequestContext(request))


def access_project(request, key):
    if not key:
        messages.error(request, "Your access key is invalid")
        return HttpResponseRedirect('/')
    
    try:
        student = AutoRegisteredStudent.objects.get(key=key)
        
    except AutoRegisteredStudent.DoesNotExist:
        messages.error(request, "Your access key {0} is invalid. Please check your link.".format(key))
        return HttpResponseRedirect('/')
    
    if not 'projects' in request.session:
        request.session['projects'] = [student.project.id]
    else:
        request.session['projects'].append(student.project.id)
    
    request.session['student'] = student
    return HttpResponseRedirect('/project/{0}'.format(student.project.id))


def request_access(request, project_id):

    project = get_object_or_404(Project, pk=project_id)

    if not project.is_upload_open():
        messages.error(request, "It's too late, submissions for this project are now closed.")
        return HttpResponseRedirect('/project/{0}'.format(project.id))

    if request.method == 'POST':
        student = AutoRegisteredStudent(project=project)
        student_form = AutoRegisteredStudentForm(request.POST, instance=student)

        if student_form.is_valid():
            student_form.save()
            student.gen_key()
            send_mail(  'Access link: {0}'.format(project),
                        '{0}access/{1}'.format(settings.SITE_URL, student.key),
                        settings.SENDER,
                        [student.email, settings.SENDER],
                        fail_silently=False)
            logging.info(" -- access key {0} sent to {1}".format(student.key, student.email))
            messages.success(request, "Please check your e-mail at {0} for your access link to {1}.".format(student.email, project))
            return HttpResponseRedirect('/')

    else:
        student_form = AutoRegisteredStudentForm()

    return render_to_response('hcstudyprojects/register.html',
        { 'student_form': student_form,
          'project': project },
        context_instance = RequestContext(request))


def answer_question(request, question_id):

    question = get_object_or_404(ProjectQuestion, pk=question_id)
    student = request.session['student']

    if not 'projects' in request.session or \
        not question.project.id in request.session['projects']:
        messages.error(request, "We were not able to authenticate you. Please re-connect.")
        return HttpResponseRedirect('/')

    if not question.project.is_upload_open():
        messages.error(request, "It's too late, submissions for this project are now closed.")
        return HttpResponseRedirect('/project/{0}'.format(question.project.id))

    try:
        answer = student.studentanswer_set.get(question=question)

    except StudentAnswer.DoesNotExist:
        answer = StudentAnswer(question=question, student=student)

    answer_form = StudentAnswerForm()


def answer_question_with_file(request, question_id):

    question = get_object_or_404(ProjectQuestion, pk=question_id)
    student = request.session['student']

    if not 'projects' in request.session or \
        not question.project.id in request.session['projects']:
        messages.error(request, "We were not able to authenticate you. Please re-connect.")
        return HttpResponseRedirect('/')

    if not question.project.is_upload_open():
        messages.error(request, "It's too late, submissions for this project are now closed.")
        return HttpResponseRedirect('/project/{0}'.format(question.project.id))
