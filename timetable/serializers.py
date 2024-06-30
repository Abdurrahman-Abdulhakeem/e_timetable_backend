from rest_framework import serializers

from .models import *

class FacultySerializer(serializers.ModelSerializer):
    acronym = serializers.CharField(read_only=True)
    
    class Meta:
        model = Faculty
        fields = (
            'id',
            'name',
            'acronym'
        )
        
class DepartmentSerializer(serializers.ModelSerializer):
    faculty = serializers.CharField(read_only=True)
    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'faculty'
        )

class LevelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Level
        fields = (
            'id',
            'name'
        )
        
class DaySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Day
        fields = (
            'id',
            'name'
        )
        
class SemesterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Semester
        fields = (
            'id',
            'name'
        )
        
class SessionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Session
        fields = (
            'id',
            'years_name'
        )
        
        
class TimetableEntrySerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()
    department = DepartmentSerializer()
    level = LevelSerializer()
    day = DaySerializer()
    semester = SemesterSerializer()
    session = SessionSerializer()
    
    class Meta:
        model = TimetableEntry
        fields = (
                'id',
                'faculty',
                'department',
                'level',
                'course',
                'course_code',
                'instructor',
                'room',
                'day',
                'start_time',
                'end_time',
                'session',
                'semester',)
     
    def create(self, validated_data):

        get_faculty = validated_data.pop('faculty')
        get_department = validated_data.pop('department')
        get_level = validated_data.pop('level')
        get_day = validated_data.pop('day')
        get_session = validated_data.pop('session')
        get_semester = validated_data.pop('semester')
 
        faculty = Faculty.objects.get(name=get_faculty['name'])
        department = Department.objects.get(name=get_department['name'])
        level = Level.objects.get(name=get_level['name'])
        day = Day.objects.get(name=get_day['name'])
        session = Session.objects.get(years_name=get_session['years_name'])
        semester = Semester.objects.get(name=get_semester['name'])
        
        return TimetableEntry.objects.create(
            faculty=faculty,
            department=department,
            level=level,
            day=day,
            session=session,
            semester=semester,
            **validated_data
        )
        
    def update(self, instance, validated_data):

        get_faculty = validated_data.pop('faculty')
        get_department = validated_data.pop('department')
        get_level = validated_data.pop('level')
        get_day = validated_data.pop('day')
        get_session = validated_data.pop('session')
        get_semester = validated_data.pop('semester')
 
        faculty = Faculty.objects.get(name=get_faculty['name'])
        department = Department.objects.get(name=get_department['name'])
        level = Level.objects.get(name=get_level['name'])
        day = Day.objects.get(name=get_day['name'])
        session = Session.objects.get(years_name=get_session['years_name'])
        semester = Semester.objects.get(name=get_semester['name'])

        instance.faculty = faculty
        instance.department = department
        instance.level = level
        instance.day = day
        instance.session = session
        instance.semester = semester
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance