from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, NotFound

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

def user_can_access_course(user, course):
    """
    Check if the user can access the course
    """
    has_enrolled = user.enrolled_courses.filter(pk=course.pk).exists()
    is_course_instructor = course.instructor.username == user.username and not user.is_student
    return has_enrolled or is_course_instructor


class ModuleListView(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_pk = self.request.query_params.get('course', None)
        user = self.request.user

        if course_pk is not None:
            try:
                course = Course.objects.get(pk=course_pk)
                
                if user_can_access_course(user, course):
                    return Module.objects.filter(course=course)
                
                raise PermissionDenied("You do not have permission to access this course.")
            except Course.DoesNotExist:
                raise NotFound("Course not found.")
        return Module.objects.none()


class ModuleDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        module_pk = self.kwargs.get('pk')
        user = self.request.user

        try:
            module = Module.objects.get(pk=module_pk)
        except Module.DoesNotExist:
            raise NotFound("Module not found.")
        
        course = module.course

        if not user_can_access_course(user, course):
            raise PermissionDenied("You do not have permission to access this course.")

        return Module.objects.filter(pk=module_pk)

class LessionListView(generics.ListCreateAPIView):
    serializer_class = LessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        module_pk = self.request.query_params.get('module', None)
        user = self.request.user
        
        if module_pk is not None:
            try:
                module = Module.objects.get(pk=module_pk)
                course = module.course

                if user_can_access_course(user, course):
                    return Lession.objects.filter(module=module)
            
                raise PermissionDenied("You do not have permission to access this course.")
            
            except Module.DoesNotExist:
                raise NotFound("Module not found.")
            
        return Lession.objects.none()


class LessionDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = LessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lession_pk = self.kwargs.get('pk')
        user = self.request.user

        try:
            lession = Lession.objects.get(pk=lession_pk)
        except Lession.DoesNotExist:
            raise NotFound("Lession not found.")
        
        course = lession.module.course

        if not user_can_access_course(user, course):
            raise PermissionDenied("You do not have permission to access this course.")

        return Lession.objects.filter(pk=lession_pk)

class AssignmentListView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        module_pk = self.request.query_params.get('module', None)
        user = self.request.user

        if module_pk is not None:
            try:
                module = Module.objects.get(pk=module_pk)
                course = module.course

                if user_can_access_course(user, course):
                    return Assignment.objects.filter(module=module)
            
                raise PermissionDenied("You do not have permission to access this course.")
            except Module.DoesNotExist:
                raise NotFound("Module not found.")
            
        return Assignment.objects.none()


class AssignmentDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        assignment_pk = self.kwargs.get('pk')
        user = self.request.user

        try:
            assignment = Assignment.objects.get(pk=assignment_pk)
        except Assignment.DoesNotExist:
            raise NotFound("Assignment not found.")
        
        course = assignment.module.course

        if not user_can_access_course(user, course):
            raise PermissionDenied("You do not have permission to access this course.")
        
        return Assignment.objects.filter(pk=assignment_pk)


class SubmissionListView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        assignment_pk = self.request.query_params.get('assignment', None)
        user = self.request.user

        if assignment_pk is not None:
            try:
                assignment = Assignment.objects.get(pk=assignment_pk)
                course = assignment.module.course

                if user_can_access_course(user, course):
                    return Submission.objects.filter(assignment=assignment)
                
                raise PermissionDenied("You do not have permission to access this course.")
            except Assignment.DoesNotExist:
                raise NotFound("Assignment not found.")
            
        return Submission.objects.none()


class SubmissionDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        submission_pk = self.kwargs.get('pk')
        user = self.request.user

        try:
            submission = Submission.objects.get(pk=submission_pk)
        except Submission.DoesNotExist:
            raise NotFound("Submission not found.")

        course = submission.assignment.module.course

        if not user_can_access_course(user, course):
            raise PermissionDenied("You do not have permission to access this course.")
        
        return Submission.objects.filter(pk=submission_pk)


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