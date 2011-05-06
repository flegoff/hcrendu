from hcrendu.hcstudyprojects.models import Project, ProjectQuestion, StudentFile, StudentAnswer, AutoRegisteredStudent

from django.contrib import admin

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'email_endswith', 'upload_opens_at', 'upload_ends_at', )

admin.site.register(Project, ProjectAdmin)

class ProjectQuestionAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'date_updated', )

admin.site.register(ProjectQuestion, ProjectQuestionAdmin)

class AutoRegisteredStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', )

admin.site.register(AutoRegisteredStudent, AutoRegisteredStudentAdmin)
admin.site.register(StudentFile)

class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'student', 'date_updated', )

admin.site.register(StudentAnswer, StudentAnswerAdmin)
