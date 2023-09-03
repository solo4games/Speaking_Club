import csv
from django.http import HttpResponse
from django.contrib import admin
from speaking_clubs import models
from django.db.models import Q


if not hasattr(admin, "display"):
    def display(description):
        def decorator(fn):
            fn.short_description = description
            return fn
        return decorator
    setattr(admin, "display", display)


class UserLevelFilter(admin.SimpleListFilter):
    title = 'Уровень'
    parameter_name = 'Уровень'

    def lookups(self, request, model_admin):
        def _get_group(student: models.Student):
            try:
                res = (student.chat.first().group.level, student.chat.first().group.level)
                if all(res):
                    return res
            except AttributeError:
                pass
        res = [
            _get_group(el) for el in models.Student.objects.all()
        ]

        res = [el for el in res if el]

        return res

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(chat__group__level__name=value)
        return queryset


class UserTeacherFilter(admin.SimpleListFilter):
    title = 'Куратор'
    parameter_name = 'Куратор'

    def lookups(self, request, model_admin):

        def _get_teacher(student: models.Student):
            try:
                res = (student.chat.first().teacher, student.chat.first().teacher)
                if all(res):
                    return res
            except AttributeError:
                pass

        res = [
            _get_teacher(el) for el in models.Student.objects.all()
        ]

        res = [el for el in res if el]

        return res

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(
                chat__teacher__email=value.split()[-1],
                chat__teacher__name=(" ".join(value.split()[:-1])),
            )
        return queryset


class UserTGFilter(admin.SimpleListFilter):
    title = 'Ник в TG'
    parameter_name = 'Ник в TG'

    def lookups(self, request, model_admin):
        res = [
            (el.user.username, el.user.username) for el in models.Student.objects.all()
        ]

        res = [el for el in res if el]

        return res

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(user__username=value)
        return queryset


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Экспорт в CSV"


class ExportStudent(ExportCsvMixin):
    list_display = [
        'id',
        'email',
        'name',
        'get_user_level',
        'get_user_teacher',
        'get_user_chat_url',
        'get_user_tg',
        'is_paid',
        'stream',
        'is_done_by_manager',
    ]

    def export_as_csv(self, request, queryset):

        meta = self.model._meta

        field_names = [
            "№",
            "Почта",
            "Имя",
            "Уровень",
            "Куратор",
            "Ссылка на чат",
            "Telegram",
            "С оплатой",
            "Поток",
            "Обработан",
        ]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        list_display_extended = ExportStudent.list_display

        def _getattr_or_call(obj, field):
            try:
                return getattr(obj, field)()
            except TypeError:
                return getattr(obj, field)

        for obj in queryset:
            row = writer.writerow([_getattr_or_call(obj, field) for field in list_display_extended])

        return response


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin, ExportStudent):
    list_display = ExportStudent.list_display
    list_filter = (
        'is_paid',
        'email',
        'name',
        'stream',
        UserLevelFilter,
        UserTeacherFilter,
        UserTGFilter,
        'is_done_by_manager',
    )
    actions = ["export_as_csv"]

    def get_user_level(self, obj):
        return obj.get_user_level()

    def get_user_teacher(self, obj):
        return obj.get_user_teacher()

    def get_user_chat_url(self, obj):
        return obj.get_user_chat_url()

    def get_user_tg(self, obj):
        return obj.get_user_tg()

    get_user_level.short_description = 'Уровень'
    get_user_teacher.short_description = 'Куратор'
    get_user_chat_url.short_description = 'Ссылка на чат'
    get_user_tg.short_description = 'Telegram'


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'name',
    )
    list_filter = list_display


@admin.register(models.Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    list_filter = list_display


@admin.register(models.Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'gc_name',
    )
    list_filter = list_display


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'level',
        'weekdays',
        'time',
    )

    list_filter = list_display


class ChatHasSudentsFilter(admin.SimpleListFilter):
    title = 'Есть студенты'
    parameter_name = 'Есть студенты'

    def lookups(self, request, model_admin):
        return (
            ('Есть', 'Есть'),
            ('Нет', 'Нет'),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == 'Есть':
            return queryset.exclude(students=None)
        else:
            return queryset.exclude(~Q(students=None))


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'group',
        'teacher',
        'chat',
        'stream',
        'get_students_count',
    )

    list_filter = (
        'group__level',
        'group__weekdays',
        'group__time',
        'chat',
        'teacher',
        'stream',
        ChatHasSudentsFilter,
    )

    @admin.display(description='Кол-во учеников')
    def get_students_count(self, obj):
        return f"{obj.students_count()}/3"


@admin.register(models.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'period',
        'description',
        'price',
    )
    list_filter = list_display


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number',
        'offer',
        'user',
        'email',
        'time',
        'weekdays',
    )
    list_filter = list_display


@admin.register(models.OrderGC)
class OrderGCAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number',
        'email',
        'stream',
    )
    list_filter = list_display


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'quiz_id',
        'answer',
    )
    list_filter = list_display
