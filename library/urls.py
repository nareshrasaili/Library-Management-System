from django.urls import path
from . import views

urlpatterns = [
    path('api/add-student/', views.add_student, name='add_student'),
    path('api/add-book/', views.add_book, name='add_book'),
    path('api/login/', views.librarian_login, name='librarian_login'),
    path('api/search-book/', views.search_book, name='search_book'),
    path('api/search-student/', views.search_student, name='search_student'),
    path('api/remove-student/', views.remove_student, name='remove_student'),
    path('api/issue-book/', views.issue_book, name='issue_book'),
    path('api/return-book/', views.return_book, name='return_book'),
    path('api/dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
]