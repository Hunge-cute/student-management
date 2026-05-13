from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError
from .models import Registration
from .serializers import RegistrationSerializer
from accounts.views import IsAdminOrStaff


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.select_related('student', 'course').all()
    serializer_class = RegistrationSerializer
    filterset_fields = ('status', 'student', 'course')
    search_fields = ('student__student_code', 'student__full_name', 'course__course_code', 'course__course_name')

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrStaff()]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        registered_count = Registration.objects.filter(course=course, status__in=['registered', 'confirmed']).count()
        if registered_count >= course.max_students:
            raise serializers.ValidationError('Môn học đã đủ sĩ số tối đa')
        serializer.save()

    def perform_destroy(self, instance):
        from tuition.models import TuitionPayment
        if TuitionPayment.objects.filter(registration=instance).exists():
            raise serializers.ValidationError('Không thể xóa: đăng ký này đã phát sinh học phí')
        instance.delete()

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        registration = self.get_object()
        registration.status = 'confirmed'
        registration.save()
        return Response(self.get_serializer(registration).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        registration = self.get_object()
        registration.status = 'cancelled'
        registration.save()
        return Response(self.get_serializer(registration).data)
