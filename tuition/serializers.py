from rest_framework import serializers
from .models import TuitionPayment, PaymentHistory


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = '__all__'
        read_only_fields = ('id', 'paid_at')


class TuitionPaymentSerializer(serializers.ModelSerializer):
    history = PaymentHistorySerializer(many=True, read_only=True)
    student_info = serializers.SerializerMethodField()

    class Meta:
        model = TuitionPayment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'history', 'student_info')

    def get_student_info(self, obj):
        return {
            'code': obj.student.student_code,
            'name': obj.student.full_name,
            'class_name': obj.student.class_name,
            'faculty': obj.student.faculty,
        }
