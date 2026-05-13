from rest_framework import serializers
from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    student_info = serializers.SerializerMethodField()
    course_info = serializers.SerializerMethodField()

    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ('id', 'registered_date', 'student_info', 'course_info')

    def get_student_info(self, obj):
        return {
            'code': obj.student.student_code,
            'name': obj.student.full_name,
            'class_name': obj.student.class_name,
            'faculty': obj.student.faculty,
        }

    def get_course_info(self, obj):
        return {
            'code': obj.course.course_code,
            'name': obj.course.course_name,
            'credits': obj.course.credits,
            'tuition_fee': str(obj.course.tuition_fee),
        }
