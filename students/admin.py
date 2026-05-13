from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_code', 'full_name', 'class_name', 'faculty', 'status')
    list_filter = ('status', 'faculty', 'course_year')
    search_fields = ('student_code', 'full_name', 'email')
