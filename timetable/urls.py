from django.urls import path

from .views import *

urlpatterns = [
    path('faculties/', FacultyView.as_view()),
    path('faculty/<int:id>/', FacultyDetailView.as_view()),
    path('departments/', DepartmentView.as_view()),
    path('department/<int:id>/', DepartmentDetailView.as_view()),
    path('timetables/', TimetableView.as_view()),
    path('timetable/entry/', TimetableCreateView.as_view()),
    
    path('days/', DayView.as_view()),
    path('semesters/', SemesterView.as_view()),
    path('levels/', LevelView.as_view()),
    path('sessions/', SessionView.as_view()),
    
    path('timetable/<int:id>/', TimetableDetailView.as_view()),
    
    
    
]