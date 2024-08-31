from django.urls import path

from .views import TransactionListView

urlpatterns = [
    path('transaction/', TransactionListView.as_view(), name='transaction'),
]