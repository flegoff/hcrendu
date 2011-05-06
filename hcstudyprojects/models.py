# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm
from django import forms
from django.conf import settings
from django.core.mail import send_mail

from datetime import datetime

import time
import hashlib
import logging

class Project(models.Model):
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    upload_opens_at = models.DateTimeField()
    upload_ends_at = models.DateTimeField()
    active = models.BooleanField(default=True, verbose_name="Shall this project be listed ?")
    email_endswith = models.CharField(max_length=75, verbose_name="Students e-mail should end with this domain")
    reupload = models.BooleanField(verbose_name="May a student delete and re-upload a file ?", default=False)
    title = models.CharField(max_length=120)
    subject = models.TextField(blank=True)

    def is_upload_open(self):
        """ Shall we accept submission for this project, right now ?"""
        now = datetime.now()
        if now > self.upload_opens_at and now < self.upload_ends_at:
            return True
        return False

    def __unicode__(self):
        return self.title

    def set_student(self, student):
        self._student = student

    def get_questions_answers(self):
        qa = {}

        for question in self.projectquestion_set.all():
            qa[question.id] = {
                'question': question,
                'answers': question.studentanswer_set.filter(student=self._student).all()
            }

        return qa


class ProjectQuestion(models.Model):
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=120)
    subject = models.TextField(blank=True)
    allow_file = models.BooleanField(default=False)
    allow_answer = models.BooleanField(default=False)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "{0} {1}".format(self.project, self.title)

    def get_answers(self):
        try:
            return self.studentanswer_set.filter(student=self.project._student).all()
        except AttributeError:
            logging.error("AttributeError")
            return None

class AutoRegisteredStudent(models.Model):
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    email = models.EmailField()
    email_validated = models.BooleanField(default=False)
    name = models.CharField(max_length=75)
    surname = models.CharField(max_length=75)
    project = models.ForeignKey(Project)
    key = models.CharField(max_length=45, blank=True)

    def __unicode__(self):
        return self.email

    def gen_key(self):
        self.save()
        self.key = "{0}{1}".format(self.id, hashlib.sha1("{0}{1}".format(settings.SECRET_KEY, self.project.id)).hexdigest())
        self.save()

    def get_answer(self, question):
        return self.studentanswer_set.filter(question=question)

    def send_invite(self):
        send_mail(  'Access link: {0}'.format(self.project),
            '{0}access/{1}'.format(settings.SITE_URL, self.key),
            settings.SENDER,
            [self.email, settings.SENDER],
            fail_silently=False)


class AutoRegisteredStudentForm(ModelForm):

    def clean_email(self):
        if not self.cleaned_data['email'].endswith(self.instance.project.email_endswith):
            raise forms.ValidationError("Your e-mail should end with {0}".format(self.instance.project.email_endswith))
        return self.cleaned_data['email']

    class Meta:
        model = AutoRegisteredStudent
        fields = ('email', 'name', 'surname', )

def get_student_file_path(instance, filename):
    return '/'.join(['uploads', instance.question.project.slug, "student-{0}".format(instance.student.id), "{0}.{1}".format(time.time(), filename)])

class StudentFile(models.Model):
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    student = models.ForeignKey(AutoRegisteredStudent)
    question = models.ForeignKey(ProjectQuestion)
    file = models.FileField(upload_to=get_student_file_path)

    def __unicode__(self):
        return "{0} {1}".format(self.student, self.question)

class StudentFileForm(ModelForm):
    class Meta:
        model = StudentFile
        fields = ('file', )

class StudentAnswer(models.Model):
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    student = models.ForeignKey(AutoRegisteredStudent)
    question = models.ForeignKey(ProjectQuestion)
    title = models.CharField(max_length=120, blank=True)
    answer = models.TextField()

    def __unicode__(self):
        return "{0} {1}".format(self.student, self.question)

class StudentAnswerForm(ModelForm):
    class Meta:
        model = StudentAnswer
        fields = ('answer', )
