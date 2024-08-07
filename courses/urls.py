from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    CategoryListView, CategoryDetailView,
    CourseListView,  CourseDetailView, MyCourseListView,
    ModuleListView, ModuleDetailView,
    LessionListView, LessionDetailView,
    AssignmentListView, AssignmentDetailView,
    SubmissionListView, SubmissionDetailView,
    EnrollListView
)


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('my-courses/', MyCourseListView.as_view(), name='my-course-list'),

    path('modules/', ModuleListView.as_view(), name='module-for-course'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='moudle-detail'),

    path('lessions/', LessionListView.as_view(), name='lessions-for-module'),
    path('lessions/<int:pk>/', LessionDetailView.as_view(), name='lession-detail'),
    
    path('assignments/', AssignmentListView.as_view(), name='assignment-for-module'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),

    path('submissions/', SubmissionListView.as_view(), name='submission-for-assignment'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),

    path('enrolls/', EnrollListView.as_view(), name='enroll-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)