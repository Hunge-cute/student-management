from django.contrib import admin
from .models import TuitionPayment, PaymentHistory


class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0
    readonly_fields = ('paid_at',)


@admin.register(TuitionPayment)
class TuitionPaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'academic_year', 'total_amount', 'paid_amount', 'remaining_amount', 'status', 'due_date')
    list_filter = ('status', 'semester', 'academic_year')
    search_fields = ('student__student_code', 'student__full_name')
    inlines = [PaymentHistoryInline]


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('payment', 'amount', 'payment_method', 'paid_by', 'paid_at')
    list_filter = ('payment_method',)
