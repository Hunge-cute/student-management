from django.db import models
from students.models import Student
from registrations.models import Registration


class TuitionPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Tiền mặt'),
        ('transfer', 'Chuyển khoản'),
        ('card', 'Thẻ tín dụng'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Chưa thanh toán'),
        ('partial', 'Đã thanh toán một phần'),
        ('paid', 'Đã thanh toán'),
        ('overdue', 'Quá hạn'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments', verbose_name='Sinh viên')
    registration = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments', verbose_name='Đăng ký')
    semester = models.CharField('Học kỳ', max_length=20)
    academic_year = models.CharField('Năm học', max_length=20)
    total_amount = models.DecimalField('Tổng học phí', max_digits=12, decimal_places=0)
    paid_amount = models.DecimalField('Đã đóng', max_digits=12, decimal_places=0, default=0)
    remaining_amount = models.DecimalField('Còn lại', max_digits=12, decimal_places=0)
    due_date = models.DateField('Hạn đóng')
    payment_method = models.CharField('Hình thức', max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    status = models.CharField('Trạng thái', max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField('Ghi chú', blank=True)
    paid_at = models.DateTimeField('Ngày đóng', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tuition_payments'
        verbose_name = 'Học phí'
        verbose_name_plural = 'Học phí'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.student_code} - {self.semester} ({self.get_status_display()})'


class PaymentHistory(models.Model):
    payment = models.ForeignKey(TuitionPayment, on_delete=models.CASCADE, related_name='history', verbose_name='Học phí')
    amount = models.DecimalField('Số tiền', max_digits=12, decimal_places=0)
    payment_method = models.CharField('Hình thức', max_length=20, choices=TuitionPayment.PAYMENT_METHOD_CHOICES)
    reference_code = models.CharField('Mã tham chiếu', max_length=100, blank=True)
    note = models.TextField('Ghi chú', blank=True)
    paid_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, verbose_name='Người thu')
    paid_at = models.DateTimeField('Ngày thu', auto_now_add=True)

    class Meta:
        db_table = 'payment_history'
        verbose_name = 'Lịch sử thanh toán'
        verbose_name_plural = 'Lịch sử thanh toán'
        ordering = ['-paid_at']

    def __str__(self):
        return f'{self.payment.student.student_code} - {self.amount}đ ({self.paid_at.date()})'
