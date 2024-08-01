from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    CategoryListView, CategoryDetailView,
    CourseListView,  CourseDetailView,
    ModuleListView, ModuleDetailView,


)


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('modules/', ModuleListView.as_view(), name='module-for-course'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='moudle-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)