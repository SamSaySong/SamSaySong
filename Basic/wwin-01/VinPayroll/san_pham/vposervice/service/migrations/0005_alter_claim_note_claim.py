# Generated by Django 3.2.6 on 2021-08-23 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_claim_note_claim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='note_claim',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
