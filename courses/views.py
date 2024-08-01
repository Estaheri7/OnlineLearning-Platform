from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import (
    CategorySerializer, CategoryDetailSerializer,
    CourseSerializer, CourseDetailSerializer,
    ModuleSerializer,
    LessionSerializer, AssignmentSerializer, SubmissionSerializer
)
from .models import (
    Category, Course, Module, Lession, Assignment, Submission
)


class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryDetailSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategoryDetailSerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

class CourseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseDetailSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CourseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseDetailSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseSerializer(course, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        

class ModuleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            course_pk = request.query_params.get('course', -1) # by queryparams course=id
            course = Course.objects.get(pk=course_pk)
            modules = Module.objects.filter(course=course)
            serializer = ModuleSerializer(modules, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ModuleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            module = Module.objects.get(pk=pk)
            serializer = ModuleSerializer(module)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Module.DoesNotExist:
            return Response({'detail': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            module = Module.objects.get(pk=pk)
            serializer = ModuleSerializer(module, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Module.DoesNotExist:
            return Response({'detail': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)


class LessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            module_pk = request.query_params.get('module', -1)
            module = Module.objects.get(pk=module_pk)
            lessions = Lession.objects.filter(module=module)
            serializer = LessionSerializer(lessions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Module.DoesNotExist:
            return Response({'detail': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        serializer = LessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            lession = Lession.objects.get(pk=pk)
            serializer = LessionSerializer(lession)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Lession.DoesNotExist:
            return Response({'detail': 'Lession not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            lession = Lession.objects.get(pk=pk)
            serializer = LessionSerializer(lession, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errros, status=status.HTTP_400_BAD_REQUEST)
        except Lession.DoesNotExist:
            return Response({'detail': 'Lession not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class AssignmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            module_pk = request.query_params.get('module', -1)
            module = Module.objects.get(pk=module_pk)
            assignments = Assignment.objects.filter(module=module)
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Module.DoesNotExist:
            return Response({'detail': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)