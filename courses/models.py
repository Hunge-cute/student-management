from django.db import models


class TuitionConfig(models.Model):
    price_per_credit = models.DecimalField('Giá 1 tín chỉ', max_digits=10, decimal_places=0, default=500000)
    summer_multiplier = models.DecimalField('Hệ số học kỳ hè', max_digits=4, decimal_places=2, default=1.50)
    is_active = models.BooleanField('Kích hoạt', default=True)
    updated_at = models.DateTimeField('Cập nhật', auto_now=True)

    class Meta:
        db_table = 'tuition_config'
        verbose_name = 'Cấu hình học phí'
        verbose_name_plural = 'Cấu hình học phí'

    def __str__(self):
        return f'Giá {self.price_per_credit}đ/tín chỉ (Hè x{self.summer_multiplier})'


class Course(models.Model):
    SEMESTER_CHOICES = [
        ('1', 'Học kỳ 1'),
        ('2', 'Học kỳ 2'),
        ('3', 'Học kỳ 3 (Hè)'),
    ]
    course_code = models.CharField('Mã môn', max_length=20, unique=True)
    course_name = models.CharField('Tên môn', max_length=200)
    credits = models.IntegerField('Số tín chỉ')
    faculty = models.CharField('Khoa', max_length=100)
    semester = models.CharField('Học kỳ', max_length=10, choices=SEMESTER_CHOICES)
    academic_year = models.CharField('Năm học', max_length=20, help_text='VD: 2025-2026')
    tuition_fee = models.DecimalField('Học phí', max_digits=12, decimal_places=0, default=0, editable=False)
    max_students = models.IntegerField('Sĩ số tối đa', default=50)
    description = models.TextField('Mô tả', blank=True)
    is_active = models.BooleanField('Kích hoạt', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'
        verbose_name = 'Môn học'
        verbose_name_plural = 'Môn học'
        ordering = ['course_code']

    def save(self, *args, **kwargs):
        config = TuitionConfig.objects.filter(is_active=True).first()
        if config:
            base = self.credits * config.price_per_credit
            if self.semester == '3':
                self.tuition_fee = int(base * config.summer_multiplier)
            else:
                self.tuition_fee = base
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.course_code} - {self.course_name}'
