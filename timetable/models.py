from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=250)
    fullname = models.CharField(max_length=250)
    
    def __str__(self):
        return self.username
    
class Faculty(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    acronym = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Department(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Semester(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Session(models.Model):
    years_name = models.CharField(max_length=100)

    def __str__(self):
        return self.years_name

class Day(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name}" 
    
class TimetableEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    course = models.CharField(max_length=200)
    course_code = models.CharField(max_length=100)
    instructor = models.CharField(max_length=200)
    room = models.CharField(max_length=200, null=True, blank=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.level} {self.department} {self.semester} {self.session} timetable entry object'
    