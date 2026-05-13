from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from .models import TuitionPayment, PaymentHistory
from .serializers import TuitionPaymentSerializer, PaymentHistorySerializer
from accounts.views import IsAdminOrStaff


class TuitionPaymentViewSet(viewsets.ModelViewSet):
    queryset = TuitionPayment.objects.select_related('student').prefetch_related('history').all()
    serializer_class = TuitionPaymentSerializer
    filterset_fields = ('status', 'semester', 'academic_year', 'student')
    search_fields = ('student__student_code', 'student__full_name')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrStaff()]

    def perform_destroy(self, instance):
        if PaymentHistory.objects.filter(payment=instance).exists():
            raise serializers.ValidationError('Không thể xóa: học phí đã có lịch sử thanh toán')
        instance.delete()

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        payment = self.get_object()
        option = request.data.get('payment_option', 'custom')
        method = request.data.get('payment_method', 'cash')
        reference = request.data.get('reference_code', '')
        remaining = payment.remaining_amount

        if option == 'full':
            amount = remaining
        elif option == 'half':
            amount = remaining // 2
            if amount <= 0:
                return Response({'error': 'Số dư còn lại quá nhỏ để chia nửa'}, status=status.HTTP_400_BAD_REQUEST)
        elif option == 'eighty_twenty':
            amount = int(remaining * Decimal('0.8')) // 1000 * 1000
            if amount <= 0:
                return Response({'error': 'Số dư còn lại quá nhỏ'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                amount = int(request.data.get('amount', 0))
            except (TypeError, ValueError):
                return Response({'error': 'Số tiền không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= 0:
            return Response({'error': 'Số tiền phải lớn hơn 0'}, status=status.HTTP_400_BAD_REQUEST)
        if amount > remaining:
            return Response({'error': f'Số tiền vượt quá số còn phải đóng ({remaining:,}đ)'}, status=status.HTTP_400_BAD_REQUEST)

        min_amount = int(payment.total_amount * Decimal('0.1'))
        if amount < min_amount and amount != remaining:
            return Response({'error': f'Số tiền tối thiểu là {min_amount:,}đ (10% tổng học phí)'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            PaymentHistory.objects.create(
                payment=payment, amount=amount,
                payment_method=method, reference_code=reference,
                paid_by=request.user, note=request.data.get('note', ''),
            )
            payment.paid_amount += amount
            payment.remaining_amount = payment.total_amount - payment.paid_amount
            if payment.remaining_amount <= 0:
                payment.status = 'paid'
                payment.paid_at = timezone.now()
            elif payment.paid_amount > 0:
                payment.status = 'partial'
            payment.save()

        return Response(TuitionPaymentSerializer(payment).data)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        payment = self.get_object()
        serializer = PaymentHistorySerializer(payment.history.all(), many=True)
        return Response(serializer.data)
