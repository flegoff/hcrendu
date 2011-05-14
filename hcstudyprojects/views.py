# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
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

    if not 'student' or not 'projects' in request.session or \
        not project.id in request.session['projects']:
        messages.error(request, "We were not able to authenticate you. Please re-connect.")
        return HttpResponseRedirect('/')

    student = request.session['student']
    project.set_student(student)
    logging.error("{0}".format(project._student))

    return render_to_response('hcstudyprojects/project.html',
        { 'project': project,
          'student': student,
          'qas': project.get_questions_answers() },
        context_instance=RequestContext(request))


def project_reinvite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not request.user.is_staff:
        messages.error(request, "Operation not permitted")
        return HttpResponseRedirect('/')

    for stud in project.autoregisteredstudent_set.all():
        stud.send_invite()
        messages.success(request, "Mail sent to {0}".format(stud))

    return HttpResponseRedirect('/')


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
        messages.error(request, "Too late, submissions for this project are now closed.")
        return HttpResponseRedirect('/'.format(project.id))

    if request.method == 'POST':
        student = AutoRegisteredStudent(project=project)
        student_form = AutoRegisteredStudentForm(request.POST, instance=student)

        if student_form.is_valid():
            student_form.save()
            student.gen_key()
            student.send_invite()
            logging.info(" -- access key {0} sent to {1}".format(student.key, student.email))
            messages.success(request, "Please check your e-mail at {0} for your access link to {1}.".format(student.email, project))
            return HttpResponseRedirect('/')

    else:
        student_form = AutoRegisteredStudentForm()

    return render_to_response('hcstudyprojects/register.html',
        { 'student_form': student_form,
          'project': project },
        context_instance = RequestContext(request))


def answer_question(request, question_id, answer_id=None):

    question = get_object_or_404(ProjectQuestion, pk=question_id)
    student = request.session['student']

    if not 'projects' in request.session or \
        not question.project.id in request.session['projects']:
        messages.error(request, "We were not able to authenticate you. Please re-connect.")
        return HttpResponseRedirect('/')

    if not question.project.is_upload_open():
        messages.error(request, "Too late, submissions for this project are now closed.")
        return HttpResponseRedirect('/project/{0}'.format(question.project.id))

    if answer_id:
        try:
            answer = student.studentanswer_set.get(id=answer_id)

        except StudentAnswer.DoesNotExist:
            messages.error(request, u"This answer does not belongs to you")
            return HttpResponseRedirect('/project/{0}'.format(question.project.id))

    else:
        answer = StudentAnswer(question=question, student=student)

    if request.method == 'POST':
        answer_form = StudentAnswerForm(request.POST, instance=answer)

        if answer_form.is_valid():
            answer_form.save()
            messages.success(request, "The answer has been saved. Thank you.")
            return HttpResponseRedirect('/project/{0}'.format(question.project.id))

    else:
        answer_form = StudentAnswerForm(instance=answer)

    return render_to_response('hcstudyprojects/answer.html',
        { 'answer_form': answer_form,
          'project': question.project,
          'question': question,
          'answer_id': answer_id },
        context_instance = RequestContext(request))



def answer_question_with_file(request, question_id):

    question = get_object_or_404(ProjectQuestion, pk=question_id)
    student = request.session['student']

    if not 'projects' in request.session or \
        not question.project.id in request.session['projects']:
        messages.error(request, "We were not able to authenticate you. Please re-connect.")
        return HttpResponseRedirect('/')

    if not question.project.is_upload_open():
        messages.error(request, "Too late, submissions for this project are now closed.")
        return HttpResponseRedirect('/project/{0}'.format(question.project.id))
