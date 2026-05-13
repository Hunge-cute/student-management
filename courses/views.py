from rest_framework import viewsets, serializers
from .models import Course, TuitionConfig
from .serializers import CourseSerializer, TuitionConfigSerializer
from accounts.views import IsAdminOrStaff
from registrations.models import Registration


class TuitionConfigViewSet(viewsets.ModelViewSet):
    queryset = TuitionConfig.objects.all()
    serializer_class = TuitionConfigSerializer
    permission_classes = [IsAdminOrStaff]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrStaff]
    search_fields = ('course_code', 'course_name', 'faculty')
    filterset_fields = ('faculty', 'semester', 'academic_year', 'is_active')

    def perform_destroy(self, instance):
        if Registration.objects.filter(course=instance).exists():
            raise serializers.ValidationError('Không thể xóa: môn học đã có sinh viên đăng ký')
        instance.delete()
