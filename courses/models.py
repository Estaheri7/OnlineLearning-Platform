import os
from django.db import models

class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    avatar = models.ImageField(blank=True, upload_to='categories/')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Course(models.Model):
    category = models.ManyToManyField(Category, blank=True, related_name='courses')
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True)
    instructor = models.ForeignKey('users.CustomUser', related_name='instructed_courses', on_delete=models.CASCADE, blank=True, null=True)
    students = models.ManyToManyField('users.CustomUser', related_name='enrolled_courses', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'
        verbose_name = 'course'
        verbose_name_plural = 'courses'


class Module(models.Model):
    course = models.ForeignKey(Course, blank=False, null=False, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'modules'
        verbose_name = 'module'
        verbose_name_plural = 'modules'


def get_upload_to_lession(instance, filename):
    module = instance.module
    course = module.course
    return os.path.join('courses', str(course.id), str(module.id),  'lessions', filename)


class Lession(models.Model):
    module = models.ForeignKey(Module, blank=False, null=False, related_name='lessions', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.FileField(blank=True, null=True, upload_to=get_upload_to_lession)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessions'
        verbose_name = 'lession'
        verbose_name_plural = 'lessions'


def get_upload_to_assignments(instance, filename):
    module = instance.module
    course = module.course
    return os.path.join('courses', str(course.id), str(module.id),  'assignments', filename)


class Assignment(models.Model):
    module = models.ForeignKey(Module, blank=False, null=False, related_name='assignments', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.FileField(blank=True, null=True, upload_to=get_upload_to_assignments)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    due_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'assignments'
        verbose_name = 'assignment'
        verbose_name_plural = 'assignments'


def get_upload_to_assignments(instance, filename):
    student = instance.student
    assignment = instance.assignment
    return os.path.join('assignments', str(student.id), str(assignment.id), 'submissions', filename)


class Submission(models.Model):
    student = models.ForeignKey('users.CustomUser', blank=False, null=False, related_name='submissions', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, blank=False, null=False, on_delete=models.CASCADE)
    content = models.FileField(blank=True, null=True, upload_to=get_upload_to_assignments)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'submissions'
        verbose_name = 'submission'
        verbose_name_plural = 'submissions'