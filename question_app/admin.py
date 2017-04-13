from django.contrib import admin
from question_app.models import *



# Register your models here.

class AdminAnswerType(admin.ModelAdmin):
    list_display = [field.name for field in AnswerType._meta.fields if field.name != "id"]
    list_display_links = [field.name for field in AnswerType._meta.fields if field.name != "id"]


class AdminAnswer(admin.ModelAdmin):
    list_display = [field.name for field in Answer._meta.fields if field.name != "id"]
    list_display_links = [field.name for field in Answer._meta.fields if field.name != "id"]
    date_hierarchy = 'created'
    search_fields = ['answer']


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1
    verbose_name = 'Ваши ответы'
    exclude = ['votes']


class AdminQuestion(admin.ModelAdmin):
    list_display = [field.name for field in Question._meta.fields if field.name != "id"]
    list_display_links = [field.name for field in Question._meta.fields if field.name != "id"]
    date_hierarchy = 'created'
    search_fields = ['question']
    inlines = [AnswerInline]

    def get_queryset(self, request):
        qs = super(AdminQuestion, self).get_queryset(request)

        # если это суперпользователь - показываем все документы
        if request.user.is_superuser:
            return qs

        return qs.filter(user=request.user)


class AdminInterview(admin.ModelAdmin):
    list_display = [field.name for field in Interview._meta.fields if field.name != "id"]
    list_display_links = [field.name for field in Interview._meta.fields if field.name != "id"]
    date_hierarchy = 'created'
    search_fields = ['interview']

    def get_queryset(self, request):
        qs = super(AdminInterview, self).get_queryset(request)

        # если это суперпользователь - показываем все документы
        if request.user.is_superuser:
            return qs

        return qs.filter(added_by=request.user)

class AdminVotesResult(admin.ModelAdmin):
    list_display = [field.name for field in VotesResult._meta.fields if field.name != "id"]
    list_display_links = [field.name for field in VotesResult._meta.fields if field.name != "id"]
    date_hierarchy = 'created'



admin.site.register(AnswerType, AdminAnswerType)
admin.site.register(Answer, AdminAnswer)
admin.site.register(Question, AdminQuestion)
admin.site.register(Interview, AdminInterview)
admin.site.register(VotesResult, AdminVotesResult)
