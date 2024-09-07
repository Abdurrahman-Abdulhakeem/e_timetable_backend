from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict

from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username:
            return Response({'message': 'Enter your username'}, status=400)
        
        elif not password:
            return Response({'message': 'Enter your password'}, status=400)
        
        try:
             user = User.objects.get(username__iexact=username)
             
             pswd_check = check_password(password, user.password)
             
             if not pswd_check:
                 return Response({'message': "Invalid username or password"}, status=400)
             
             if not user.is_active:
                 return Response({'message': "Account is not active, contact admin"}, status=400)

             refresh = RefreshToken.for_user(user)
             return Response({'message':
                "Logged in successful",
                'status':True,
                'user': model_to_dict(user, ['id', 'username', 
                                             'username',
                                             ]),
                'access': str(refresh.access_token),
                'refresh': str(refresh)
                
                })  
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=404)
        
class RegisterView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        required_fields = ['email', 'username', 'password', 'fullname']
        
        for field in required_fields:
            if field not in request.data:
                return Response({"message": f"{field} is required"}, status=400)
        
        if User.objects.filter(email__iexact=request.data.get('email')).exists():
            return Response({"message": "Email already exists"}, status=400)
        if User.objects.filter(username__iexact=request.data.get('username')).exists():
            return Response({"message": "Username already taken"}, status=400)
        
        RegisterSerializer = UserSerializer(data=request.data)
        if RegisterSerializer.is_valid(raise_exception=True):
            RegisterSerializer.save()
            return Response({"message": "New admin added successfully", "data": RegisterSerializer.data}, status=201)
        return Response({"message": "Error while registering"}, status=400)
        
class UserDetailView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        
        user = request.user
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    
class UsersView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        
        qs = User.objects.all()
        
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data, status=200)

class UsersDetail(APIView):
     permission_classes = (IsAuthenticated, )
     def put(self, request, id, *args, **kwargs):
        
        try:
            obj = User.objects.get(id=id)
            serializer = UserSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                if obj.is_superuser and obj != request.user:
                    return Response({"message": "Can't alter super user"}, status=400)
                serializer.save()
                return Response({"message": "User updated successfully", "id": id, "data":serializer.data}, status=200)
        
        except Faculty.DoesNotExist:
            return Response({"message": "User does not exist"}, status=404)
     
     def delete(self, request, id, *args, **kwargs):
        try:
            obj = User.objects.get(id=id)
            if obj.is_superuser and obj != request.user:
                return Response({"message": "Can't delete super user"}, status=400)
            obj.delete()
            return Response(
                    {"message": "User deleted successfully", "id": id},
                    status=200)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=404)
    

class FacultyView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
    def get(self, request, *args, **kwargs):
        faculty = request.GET.get('faculty')
        if faculty:
            qs = Faculty.objects.filter(Q(name__icontains=faculty) |
                                        Q(acronym__icontains=faculty))
            qs_serializer = FacultySerializer(qs, many=True)
            return Response(qs_serializer.data)
        
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
            return Response({"message": "Faculty added successfully", "data" : serializer.data}, status=201)

class FacultyDetailView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def put(self, request, id, *args, **kwargs):
        
        try:
            obj = Faculty.objects.get(id=id)
            serializer = FacultySerializer(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Faculty updated successfully", "id": id, "data":serializer.data}, status=200)
        
        except Faculty.DoesNotExist:
            return Response({"message": "Faculty does not exist"}, status=404)
    
    def delete(self, request, id, *args, **kwargs):
        try:
            obj = Faculty.objects.get(id=id)
            obj.delete()
            return Response(
                    {"message": "Faculty deleted successfully", "id": id},
                    status=200)
        except Faculty.DoesNotExist:
            return Response({"message": "Faculty not found"}, status=404)
    
        
class DepartmentView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
    def get(self, request, *args, **kwargs):
        department = request.GET.get('department')
        if department:
            qs = Department.objects.filter(Q(name__icontains=department) |
                                           Q(faculty__name__icontains=department) |
                                           Q(faculty__acronym__icontains=department))
            qs_serializer = DepartmentSerializer(qs, many=True)
            return Response(qs_serializer.data)
        
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
            return Response({"message": "Department added successfully", "data": serializer.data}, status=201)

class DepartmentDetailView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def put(self, request, id, *args, **kwargs):
        
        try:
            obj = Department.objects.get(id=id)
            serializer = DepartmentSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Department updated successfully", "id": id, "data":serializer.data}, status=200)
        
        except Department.DoesNotExist:
            return Response({"message": "Department does not exist"}, status=404)
    
    def delete(self, request, id, *args, **kwargs):
        try:
            obj = Department.objects.get(id=id)
            obj.delete()
            return Response(
                    {"message": "Department deleted successfully", "id": id},
                    status=200)
        except Department.DoesNotExist:
            return Response({"message": "Department not found"}, status=404)
        
class DayView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
    def get(self, request, *args, **kwargs):
        qs = Day.objects.all()
        
        qs_serializer = DaySerializer(qs, many=True)
        return Response(qs_serializer.data)    
        
class SemesterView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
    def get(self, request, *args, **kwargs):
        qs = Semester.objects.all()
        
        qs_serializer = SemesterSerializer(qs, many=True)
        return Response(qs_serializer.data)     
    
    
    def post(self, request, *args, **kwargs):
        
        if not request.data.get('name'):
            return Response({"message": "Semester name is required"}, status=400)

        serializer = SemesterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            serializer.save()
            return Response({"message": "Semester added successfully", "data" : serializer.data}, status=201)

class SemesterDetailView(APIView):
    permission_classes = (IsAuthenticated, )
     
    def delete(self, request, id, *args, **kwargs):
        try:
            obj = Semester.objects.get(id=id)
            obj.delete()
            return Response(
                    {"message": "Semester deleted successfully", "id": id},
                    status=200)
        except Semester.DoesNotExist:
            return Response({"message": "Semester not found"}, status=404)
    
    
       
class LevelView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
    def get(self, request, *args, **kwargs):
        qs = Level.objects.all()
        
        qs_serializer = LevelSerializer(qs, many=True)
        return Response(qs_serializer.data)  
    
    def post(self, request, *args, **kwargs):
        
        if not request.data.get('name'):
            return Response({"message": "Level name is required"}, status=400)

        serializer = LevelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            serializer.save()
            return Response({"message": "Level added successfully", "data" : serializer.data}, status=201)

class LevelDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
    def delete(self, request, id, *args, **kwargs):
        try:
            obj = Level.objects.get(id=id)
            obj.delete()
            return Response(
                    {"message": "Level deleted successfully", "id": id},
                    status=200)
        except Level.DoesNotExist:
            return Response({"message": "Level not found"}, status=404)
    
    
    
          
class SessionView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
    def get(self, request, *args, **kwargs):
        qs = Session.objects.all()
        
        qs_serializer = SessionSerializer(qs, many=True)
        return Response(qs_serializer.data)  
    
    def post(self, request, *args, **kwargs):
        
        if not request.data.get('years_name'):
            return Response({"message": "Session years is required"}, status=400)

        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            serializer.save()
            return Response({"message": "Session added successfully", "data" : serializer.data}, status=201)

class SessionDetailView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def delete(self, request, id, *args, **kwargs):
        try:
            obj = Session.objects.get(id=id)
            obj.delete()
            return Response(
                    {"message": "Session deleted successfully", "id": id},
                    status=200)
        except Session.DoesNotExist:
            return Response({"message": "Session not found"}, status=404)
     
    
        


class TimetableView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
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
                                           Q(semester= 2))
        
        qs_serializer = TimetableEntrySerializer(qs, many=True)
        return Response(qs_serializer.data, status=200)
        

class TimetableCreateView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, *args, **kwargs):
        data = request.data
        # ADD COURSE AND INSTRUCTOR IN REQUIRED FIELDS LATER
        required_fields = [
                'faculty', 'department', 'level', 'course_code',
                'room', 'day', 'start_time', 'end_time', 'session', 'semester'
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
            
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            
            # Check for instructor conflict
            instructor_conflict = TimetableEntry.objects.filter(
                instructor=data['instructor'],
                day=day,
                start_time__lt=end_time,
                end_time__gt=start_time,
                session=session,
                semester=semester
            ).exists()

            if instructor_conflict:
                return Response(
                    {"message": "Instructor is already assigned to another class during this time."},
                    status=400
                )

            # Check for room conflict
            room_conflict = TimetableEntry.objects.filter(
                room=data['room'],
                day=day,
                start_time__lt=end_time,
                end_time__gt=start_time,
                session=session,
                semester=semester
            ).exists()

            if room_conflict:
                return Response(
                    {"message": "The room is already occupied during this time."},
                    status=400
                )

            # If no conflicts, save the entry
            
            serializer.save()
            return Response({"message": "New entry timetable created", "data": serializer.data}, status=201)
        return Response(serializer.errors, status=400)
    

class TimetableDetailView(APIView):
    permission_classes = (IsAuthenticated, )
    
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