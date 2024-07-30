from django.contrib import admin
from .models import Category, Course, Module, Lession, Assignment, Submission



class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


class LessionInline(admin.TabularInline):
    model = Lession
    extra = 1


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1


class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'created_time', 'updated_time')
    search_fields = ('title',)
    list_filter = ('parent',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_time', 'updated_time')
    search_fields = ('title', 'description', 'instructor__username')
    list_filter = ('instructor', 'category')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_time', 'updated_time')
    search_fields = ('title',)
    list_filter = ('course',)
    inlines = [LessionInline, AssignmentInline]


@admin.register(Lession)
class LessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'created_time', 'updated_time')
    search_fields = ('title',)
    list_filter = ('module',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'created_time', 'updated_time', 'due_time')
    search_fields = ('title',)
    list_filter = ('module',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at')
    search_fields = ('student__username', 'assignment__title')
    list_filter = ('assignment', 'student')
