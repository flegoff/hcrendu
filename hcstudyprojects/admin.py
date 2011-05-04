from hcrendu.hcstudyprojects.models import Project, ProjectQuestion, StudentFile, StudentAnswer, AutoRegisteredStudent

from django.contrib import admin

admin.site.register(Project)
admin.site.register(ProjectQuestion)
admin.site.register(AutoRegisteredStudent)
admin.site.register(StudentFile)
admin.site.register(StudentAnswer)
