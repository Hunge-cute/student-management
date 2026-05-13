from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'registered_date', 'status')
    list_filter = ('status',)
    search_fields = ('student__student_code', 'student__full_name', 'course__course_code')
