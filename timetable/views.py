from django.shortcuts import render
from django.db.models import Q

from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class FacultyView(APIView):
    
    def get(self, request, *args, **kwargs):
        qs = Faculty.objects.all()
        
        qs_serializer = FacultySerializer(qs, many=True)
        return Response(qs_serializer.data)
    
    def post(self, request, *args, **kwargs):
        
        if not request.data.get('name'):
            return Response({"message": "Faculty name is required"}, status=400)
        
        if not request.data.get('acronym'):
            return Response({"message": "Acronym is required e.g SPAS, ..."}, status=400)

        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            serializer.save()
            return Response({"message": "Faculty added successfully"}, status=201)

class FacultyDetailView(APIView):
    
    def put(self, request, id, *args, **kwargs):
        
        try:
            obj = Faculty.objects.get(id=id)
            serializer = FacultySerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Faculty updated successfully", "data":serializer.data}, status=200)
        
        except Faculty.DoesNotExist:
            return Response({"message": "Faculty does not exist"}, status=404)
        
        
class DepartmentView(APIView):
    
    def get(self, request, *args, **kwargs):
        qs = Department.objects.all()
        
        qs_serializer = DepartmentSerializer(qs, many=True)
        return Response(qs_serializer.data)
    
    def post(self, request, *args, **kwargs):
        
        if not request.data.get('name'):
            return Response({"message": "Department name is required"}, status=400)
        
        if not request.data.get('faculty'):
            return Response({"message": "Faculty is required e.g SPAS, ..."}, status=400)

        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            serializer.save()
            return Response({"message": "Department added successfully"}, status=201)

class DepartmentDetailView(APIView):
    
    def put(self, request, id, *args, **kwargs):
        
        try:
            obj = Department.objects.get(id=id)
            serializer = DepartmentSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Department updated successfully", "data":serializer.data}, status=200)
        
        except Department.DoesNotExist:
            return Response({"message": "Department does not exist"}, status=404)
        
class DayView(APIView):
    
    def get(self, request, *args, **kwargs):
        qs = Day.objects.all()
        
        qs_serializer = DaySerializer(qs, many=True)
        return Response(qs_serializer.data)    
        
class SemesterView(APIView):
    
    def get(self, request, *args, **kwargs):
        qs = Semester.objects.all()
        
        qs_serializer = SemesterSerializer(qs, many=True)
        return Response(qs_serializer.data)     
       
class LevelView(APIView):
    
    def get(self, request, *args, **kwargs):
        qs = Level.objects.all()
        
        qs_serializer = LevelSerializer(qs, many=True)
        return Response(qs_serializer.data)  
          
class SessionView(APIView):
    
    def get(self, request, *args, **kwargs):
        qs = Session.objects.all()
        
        qs_serializer = SessionSerializer(qs, many=True)
        return Response(qs_serializer.data)        


class TimetableView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        faculty = request.GET.get('faculty')
        department = request.GET.get('department')
        level = request.GET.get('level')
        session = request.GET.get('session')
        semester = request.GET.get('semester')
        
        if faculty and department and level and session and semester:
            qs = TimetableEntry.objects.filter(Q(faculty__name=faculty) &
                                               Q(department=department) &
                                               Q(level=level) &
                                               Q(session=session) &
                                               Q(semester=semester))
            qs_serializer = TimetableEntrySerializer(qs, many=True)
            return Response(qs_serializer.data, status=200)
        
        session = Session.objects.first()
    
        qs = TimetableEntry.objects.filter(Q(faculty= 1) & 
                                           Q(department= 1) &
                                           Q(level= 1) &
                                           Q(session=session) &
                                           Q(semester= 1))
        
        qs_serializer = TimetableEntrySerializer(qs, many=True)
        return Response(qs_serializer.data, status=200)
        

class TimetableCreateView(APIView):
    
    def post(self, request, *args, **kwargs):
        data = request.data
        required_fields = [
                'faculty', 'department', 'level', 'course', 'course_code',
                'instructor', 'room', 'day', 'start_time', 'end_time', 'session', 'semester'
            ]

            # Check if all required fields are present
        for field in required_fields:
            if field not in data:
                return Response(
                    {f'message': f'{field} is required'},
                    status=400
                )
        try:
            faculty = Faculty.objects.get(name=data['faculty']['name'])
            department = Department.objects.get(name=data['department']['name'])
            level = Level.objects.get(name=data['level']['name'])
            day = Day.objects.get(name=data['day']['name'])
            session = Session.objects.get(years_name=data['session']['years_name'])
            semester = Semester.objects.get(name=data['semester']['name'])
            
        except (Faculty.DoesNotExist, Department.DoesNotExist, Level.DoesNotExist,
                Day.DoesNotExist, Session.DoesNotExist,
                Semester.DoesNotExist) as e:
            return Response(
            {'message': str(e)},
            status=400
        )
        serializer = TimetableEntrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New entry timetable created", "data": serializer.data}, status=201)
        return Response(serializer.errors, status=400)
    

class TimetableDetailView(APIView):
    
    def put(self, request, id, *args, **kwargs):
        
        try:
            obj = TimetableEntry.objects.get(id=id)
            serializer = TimetableEntrySerializer(obj, request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {"message": "Timetable entry updated successfully",
                     "data": serializer.data, "id": id}
                    , status=200)
        except TimetableEntry.DoesNotExist:
            return Response({"message": "Timetable entry not found"}, status=404)
    
    def delete(self, request, id, *args, **kwargs):
        try:
            obj = TimetableEntry.objects.get(id=id)
            obj.delete()
            return Response(
                    {"message": "Timetable entry deleted successfully", "id": id},
                    status=200)
        except TimetableEntry.DoesNotExist:
            return Response({"message": "Timetable entry not found"}, status=404)