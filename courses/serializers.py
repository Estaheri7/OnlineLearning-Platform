from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from .models import Category, Course, Module, Lession, Assignment, Submission
from users.serializers import CustomUserSerializer
from users.models import CustomUser



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'parent', 'title', 'avatar', 'created_time', 'updated_time')


class CategoryDetailSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'parent', 'title', 'avatar', 'created_time', 'updated_time')

    def get_parent(self, obj):
        if obj.parent:
            return CategoryDetailSerializer(obj.parent).data
        return None


class CourseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )

    class Meta:
        model = Course
        fields = ('id', 'category', 'title', 'description', 'avatar', 'instructor', 'students', 'price')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        if user.is_student:
            raise serializers.ValidationError({"instructor": "User is not an authorized instructor."})
        
        if 'instructor' not in validated_data:
            validated_data['instructor'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        instructor = instance.instructor

        if (user.is_student) or (user.username != instructor.username):
            raise PermissionDenied('You do not have permission to update this submission.')
        return super().update(instance, validated_data)

class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    instructor = CustomUserSerializer()
    students = CustomUserSerializer(many=True)

    class Meta:
        model = Course
        fields = ('id', 'category', 'title', 'description', 'avatar', 'instructor', 'students', 'price', 'created_time', 'updated_time')


class ModuleSerializer(serializers.ModelSerializer):
    lessions = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ('id', 'course', 'title', 'lessions', 'created_time', 'updated_time')

    def get_lessions(self, obj):
        serializer = LessionSerializer(obj.lessions.all(), many=True)
        data = serializer.data
        return [id_['id'] for id_ in data]
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        course = instance.course
        instructor = course.instructor

        if (user.is_student) or (user.username != instructor.username):
            raise PermissionDenied('You do not have permission to update this submission.')
        return super().update(instance, validated_data)


class LessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lession
        fields = ('id', 'module', 'title', 'content', 'created_time', 'updated_time')

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        module = instance.module
        course = module.course
        instructor = course.instructor

        if (user.is_student) or (user.username != instructor.username):
            raise PermissionDenied('You do not have permission to update this submission.')
        return super().update(instance, validated_data)
    

class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ('id', 'module', 'title', 'content', 'created_time', 'updated_time', 'due_time')

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        module = instance.module
        course = module.course
        instructor = course.instructor

        if (user.is_student) or (user.username != instructor.username):
            raise PermissionDenied('You do not have permission to update this submission.')
        return super().update(instance, validated_data)

    

class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = ('id', 'student', 'assignment', 'content', 'submitted_at')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        if 'student' not in validated_data:
            validated_data['student'] = user
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        student = instance.student

        if (student.username != user.username):
            raise PermissionDenied("You do not have permission to update this submission.")
        
        return super().update(instance, validated_data)
        
