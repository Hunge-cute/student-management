from django.db import models
from django.core.validators import RegexValidator


class Student(models.Model):
    STATUS_CHOICES = [
        ('studying', 'Đang học'),
        ('graduated', 'Đã tốt nghiệp'),
        ('suspended', 'Bị đình chỉ'),
        ('dropped', 'Đã thôi học'),
    ]
    student_code = models.CharField('Mã SV', max_length=20, unique=True)
    full_name = models.CharField('Họ tên', max_length=100)
    email = models.EmailField('Email', max_length=100, unique=True)
    phone = models.CharField('Điện thoại', max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    date_of_birth = models.DateField('Ngày sinh')
    gender = models.CharField('Giới tính', max_length=10, choices=[('male', 'Nam'), ('female', 'Nữ')])
    address = models.TextField('Địa chỉ', blank=True)
    class_name = models.CharField('Lớp', max_length=50)
    faculty = models.CharField('Khoa', max_length=100)
    course_year = models.IntegerField('Khóa', help_text='Năm nhập học')
    status = models.CharField('Trạng thái', max_length=20, choices=STATUS_CHOICES, default='studying')
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)

    class Meta:
        db_table = 'students'
        verbose_name = 'Sinh viên'
        verbose_name_plural = 'Sinh viên'
        ordering = ['student_code']

    def __str__(self):
        return f'{self.student_code} - {self.full_name}'
