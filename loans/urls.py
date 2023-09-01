from django.urls import path
from .views import BorrowBookView, LoanListView
urlpatterns = [
    path('', LoanListView.as_view(), name='loans' ),
    path('<str:status>/', LoanListView.as_view(), name='loans' ),
    path('borrow/<str:pk>/', BorrowBookView.as_view(), name='borrow_book' ),
]
