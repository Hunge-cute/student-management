from django.db.models import Sum, Count, Q
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from students.models import Student
from courses.models import Course
from registrations.models import Registration
from tuition.models import TuitionPayment, PaymentHistory


class ReportViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        total_students = Student.objects.count()
        active_students = Student.objects.filter(status='studying').count()
        total_courses = Course.objects.filter(is_active=True).count()
        total_registrations = Registration.objects.filter(status__in=['registered', 'confirmed']).count()

        total_revenue = TuitionPayment.objects.aggregate(
            total=Sum('total_amount'),
            paid=Sum('paid_amount'),
        )
        overdue_count = TuitionPayment.objects.filter(status='overdue').count()

        return Response({
            'total_students': total_students,
            'active_students': active_students,
            'total_courses': total_courses,
            'total_registrations': total_registrations,
            'total_revenue': str(total_revenue['total'] or 0),
            'paid_revenue': str(total_revenue['paid'] or 0),
            'overdue_count': overdue_count,
        })

    @action(detail=False, methods=['get'])
    def revenue_by_semester(self, request):
        data = (
            TuitionPayment.objects
            .values('semester', 'academic_year')
            .annotate(
                total=Sum('total_amount'),
                paid=Sum('paid_amount'),
                count=Count('id'),
            )
            .order_by('-academic_year', 'semester')
        )
        return Response(list(data))

    @action(detail=False, methods=['get'])
    def registration_stats(self, request):
        data = (
            Course.objects
            .filter(is_active=True)
            .annotate(
                registered=Count('registrations', filter=Q(registrations__status__in=['registered', 'confirmed'])),
            )
            .values('course_code', 'course_name', 'faculty', 'max_students', 'registered')
            .order_by('faculty')
        )
        return Response(list(data))

    @action(detail=False, methods=['get'])
    def tuition_status(self, request):
        data = (
            TuitionPayment.objects
            .values('status')
            .annotate(count=Count('id'), total=Sum('total_amount'), paid=Sum('paid_amount'))
        )
        return Response(list(data))

    @action(detail=False, methods=['get'])
    def overdue_list(self, request):
        overdue = (
            TuitionPayment.objects
            .filter(status='overdue')
            .select_related('student')
            .values(
                'student__student_code', 'student__full_name',
                'student__class_name', 'semester', 'academic_year',
                'total_amount', 'paid_amount', 'remaining_amount', 'due_date'
            )
        )
        return Response(list(overdue))
