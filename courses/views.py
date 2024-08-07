from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import (
    CategorySerializer, CategoryDetailSerializer,
    CourseSerializer, CourseDetailSerializer,
    ModuleSerializer,
    LessionSerializer, AssignmentSerializer, SubmissionSerializer, EnrollSerializer
)
from .models import (
    Category, Course, Module, Lession, Assignment, Submission, Enrollment
)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategorySerializer
        return CategoryDetailSerializer


class CategoryDetailView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CategorySerializer
        return CategoryDetailSerializer


class CourseListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseSerializer
        return CourseDetailSerializer
    
    def get_queryset(self):
        queryset = Course.objects.all()

        category_pk = self.request.GET.get('category')

        if category_pk:
            return queryset.filter(category=category_pk)

        return queryset


class CourseDetailView(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CourseSerializer
        return CourseDetailSerializer
        

class MyCourseListView(generics.ListAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        enrolled_courses = user.enrolled_courses.all()
        instructed_courses = user.instructed_courses.all()
        courses = enrolled_courses.union(instructed_courses)
        return courses


class ModuleListView(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_pk = self.request.query_params.get('course', None)
        if course_pk is not None:
            course = Course.objects.get(pk=course_pk)
            return Module.objects.filter(course=course)
        return Module.objects.none()


class ModuleDetailView(generics.RetrieveUpdateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]


class LessionListView(generics.ListCreateAPIView):
    serializer_class = LessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        module_pk = self.request.query_params.get('module', None)
        if module_pk is not None:
            module = Module.objects.get(pk=module_pk)
            return Lession.objects.filter(module=module)
        return Lession.objects.none()


class LessionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Lession.objects.all()
    serializer_class = LessionSerializer
    permission_classes = [IsAuthenticated]
        
        
class AssignmentListView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        module_pk = self.request.query_params.get('module', None)
        if module_pk is not None:
            module = Module.objects.get(pk=module_pk)
            return Assignment.objects.filter(module=module)
        return Assignment.objects.none()


class AssignmentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]


class SubmissionListView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        assignment_pk = self.request.query_params.get('assignment', None)
        if assignment_pk is not None:
            assignment = Assignment.objects.get(pk=assignment_pk)
            return Submission.objects.filter(assignment=assignment)
        return Submission.objects.none()


class SubmissionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]


class EnrollListView(generics.ListCreateAPIView):
    serializer_class = EnrollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Enrollment.objects.filter(user=user)
    
    def post(self, request, *args, **kwargs):
        course_pk = request.data['course']
        try:
            course = Course.objects.get(pk=course_pk)
            return super().post(request, *args, **kwargs)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)