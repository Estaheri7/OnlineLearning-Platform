from rest_framework import serializers

from .models import Category, Course, Module, Lession, Assignment, Submission
from users.serializers import CustomUserSerializer



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'parent', 'title', 'avatar', 'created_time', 'updated_time')


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    instructor = CustomUserSerializer()
    students = CustomUserSerializer()

    class Meta:
        model = Course
        fields = ('id', 'category', 'title', 'description', 'avatar', 'instructor', 'students', 'created_time',
                  'updated_time')
        

class ModuleSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Module
        fields = ('id', 'course', 'title', 'created_time', 'updated_time')


class LessionSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Lession
        fields = ('id', 'module', 'title', 'content', 'content_type', 'created_time', 'updated_time')

    def get_file_type(self, obj):
        return obj.get_file_type_display()
    

class AssignmentSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ('id', 'module', 'title', 'content', 'content_type', 'created_time', 'updated_time', 'due_time')

    def get_file_type(self, obj):
        return obj.get_file_type_display()
    

class SubmissionSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer()
    assignment = AssignmentSerializer()
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ('id', 'student', 'assignment', 'content', 'content_type', 'submitted_at')

    def get_file_type(self, obj):
        return obj.get_file_type_display()