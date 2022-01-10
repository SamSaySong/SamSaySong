# Generated by Django 3.2.6 on 2021-11-04 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_claim', models.CharField(max_length=128, unique=True)),
                ('data_claim', models.JSONField(blank=True, null=True)),
                ('company_claim', models.CharField(blank=True, max_length=128, null=True)),
                ('status_claim', models.CharField(choices=[('Complete', 'Complete'), ('Error', 'Error'), ('Running', 'Running'), ('Wait', 'Wait'), ('Stop', 'Stop')], default='Wait', max_length=100, null=True)),
                ('status_process_claim', models.CharField(choices=[('Complete', 'Complete'), ('Error', 'Error'), ('Running', 'Running'), ('Wait', 'Wait'), ('Stop', 'Stop')], default='Đã phê duyệt (nội bộ)', max_length=100, null=True)),
                ('note_claim', models.CharField(blank=True, max_length=128, null=True)),
                ('tracking_claim', models.JSONField(blank=True, null=True)),
                ('created_claim', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('updated_claim', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date updated')),
            ],
            options={
                'verbose_name_plural': '01. Danh sách yêu cầu',
            },
        ),
    ]
