from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('user/', UserDetailView.as_view()),
    
    path('users/', UsersView.as_view()),
    path('users/<int:id>/', UsersDetail.as_view()),
    path('register/', RegisterView.as_view()),
    
    path('faculties/', FacultyView.as_view()),
    path('faculty/<int:id>/', FacultyDetailView.as_view()),
    path('departments/', DepartmentView.as_view()),
    path('department/<int:id>/', DepartmentDetailView.as_view()),
    path('timetables/', TimetableView.as_view()),
    path('timetable/entry/', TimetableCreateView.as_view()),
    path('timetable/<int:id>/', TimetableDetailView.as_view()),
    
    path('days/', DayView.as_view()),
    
    path('semesters/', SemesterView.as_view()),
    path('semester/<int:id>/', SemesterDetailView.as_view()),
        
    path('levels/', LevelView.as_view()),
    path('level/<int:id>/', LevelDetailView.as_view()),
    
    path('sessions/', SessionView.as_view()),
    path('session/<int:id>/', SessionDetailView.as_view()),
    
    
    
    
]