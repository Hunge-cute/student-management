from django.contrib import admin
from .models import Course, TuitionConfig


@admin.register(TuitionConfig)
class TuitionConfigAdmin(admin.ModelAdmin):
    list_display = ('price_per_credit', 'summer_multiplier', 'is_active', 'updated_at')
    list_editable = ('is_active',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'credits', 'tuition_fee', 'faculty', 'semester', 'academic_year', 'is_active')
    list_filter = ('faculty', 'semester', 'academic_year', 'is_active')
    search_fields = ('course_code', 'course_name')
    readonly_fields = ('tuition_fee',)
