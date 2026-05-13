from django.db import models
from students.models import Student
from courses.models import Course


class Registration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Đã đăng ký'),
        ('confirmed', 'Đã xác nhận'),
        ('cancelled', 'Đã hủy'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations', verbose_name='Sinh viên')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations', verbose_name='Môn học')
    registered_date = models.DateTimeField('Ngày đăng ký', auto_now_add=True)
    status = models.CharField('Trạng thái', max_length=20, choices=STATUS_CHOICES, default='registered')
    note = models.TextField('Ghi chú', blank=True)

    class Meta:
        db_table = 'registrations'
        verbose_name = 'Đăng ký môn học'
        verbose_name_plural = 'Đăng ký môn học'
        unique_together = ('student', 'course')
        ordering = ['-registered_date']

    def __str__(self):
        return f'{self.student.student_code} - {self.course.course_code} ({self.get_status_display()})'
