from rest_framework import serializers
from .models import Course, TuitionConfig


class TuitionConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuitionConfig
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    registered_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'registered_count', 'tuition_fee')

    def get_registered_count(self, obj):
        return obj.registrations.filter(status='registered').count()
