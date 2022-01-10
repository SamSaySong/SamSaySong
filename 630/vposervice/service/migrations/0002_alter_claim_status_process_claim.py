# Generated by Django 3.2.6 on 2021-11-04 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='status_process_claim',
            field=models.CharField(choices=[('Mới', 'Mới'), ('Chờ phê duyệt (nội bộ)', 'Chờ phê duyệt (nội bộ)'), ('Đã phê duyệt (nội bộ)', 'Đã phê duyệt (nội bộ)'), ('Đã kê khai và lưu tạm hồ sơ', 'Đã kê khai và lưu tạm hồ sơ'), ('Đã ký nộp hồ sơ và nộp chứng từ cho cơ quan BHXH', 'Đã ký nộp hồ sơ và nộp chứng từ cho cơ quan BHXH'), ('Đang xử lý (tại BHXH)', 'Đang xử lý (tại BHXH)'), ('Đã có kết quả', 'Đã có kết quả')], default='Đã phê duyệt (nội bộ)', max_length=100, null=True),
        ),
    ]
