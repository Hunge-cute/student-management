from rest_framework import viewsets, serializers
from .models import Student
from .serializers import StudentSerializer
from accounts.views import IsAdminOrStaff
from registrations.models import Registration
from tuition.models import TuitionPayment


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrStaff]
    search_fields = ('student_code', 'full_name', 'email', 'phone', 'class_name', 'faculty')
    filterset_fields = ('status', 'faculty', 'class_name', 'course_year')

    def perform_destroy(self, instance):
        if Registration.objects.filter(student=instance).exists():
            raise serializers.ValidationError('Không thể xóa: sinh viên đã có đăng ký môn học')
        if TuitionPayment.objects.filter(student=instance).exists():
            raise serializers.ValidationError('Không thể xóa: sinh viên đã phát sinh học phí')
        instance.delete()
