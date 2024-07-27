from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'fullname',
            'email',
            'password'
        )
    
    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
            )
        user.set_password(validated_data.get('password'))
        return user
    
    def validate(self, obj):
        errors = {}
        if not obj.get("email").endswith(("@gmail.com", "@yahoo.com")):
            errors['message'] = "We accept only valid email addresses"
            raise serializers.ValidationError(errors)
        
        if ' ' not in obj.get('fullname').strip():
            errors['message'] = "Fullname must contain a space separating first name and last name."
            raise serializers.ValidationError(errors)
        
        return obj

class FacultySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Faculty
        fields = (
            'id',
            'name',
            'acronym'
        )
        extra_kwargs = {
            'acronym': {'required': False}
        }
        
class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(required=False)
    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'faculty'
        )
        
    def create(self, validated_data):
        
        get_faculty = validated_data.pop('faculty')
        
        if get_faculty:
            faculty = Faculty.objects.get(name=get_faculty['name'])
            validated_data['faculty'] = faculty
        return Department.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        
        get_faculty = validated_data.pop('faculty', None)
        
        if get_faculty:
            faculty = Faculty.objects.get(name=get_faculty['name'])
            instance.faculty = faculty
        for atrr, value in validated_data.items():
            setattr(instance, atrr, value)

        instance.save()
        return instance
        
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
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['start_time'] = instance.start_time.strftime('%I:%M %p')    
        rep['end_time'] = instance.end_time.strftime('%I:%M %p')
        return rep
            
    def to_internal_value(self, data):
        data['start_time'] = self.parse_time(data['start_time'])
        data['end_time'] = self.parse_time(data['end_time'])
        return super().to_internal_value(data)
    
    def parse_time(self, value):
        from datetime import datetime
        return datetime.strptime(value, '%I:%M %p').time()