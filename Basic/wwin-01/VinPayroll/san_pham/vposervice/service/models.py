# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from typing import DefaultDict

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


#-----YÊU CẦU-----------
class Claim(models.Model):
    name_claim = models.CharField(max_length=128, unique=True)
    data_claim = models.JSONField(null=True, blank=True)
    list_status_claim =[
        ('Complete', 'Complete'),
        ('Error', 'Error'),
        ('Running', 'Running'),
        ('Wait', 'Wait'),
        ('Stop', 'Stop'),
    ]
    company_claim = models.CharField(max_length=128, null=True, blank=True)
    status_claim = models.CharField(choices=list_status_claim, max_length=100, null=True, default="Wait")
    note_claim = models.CharField(max_length=128, null=True, blank=True)
    created_claim = models.DateTimeField(u"Date created", auto_now_add=True)
    updated_claim = models.DateTimeField(
        u"Date updated", auto_now=True, db_index=True)
    
    def __str__(self):
        return self.name_claim +" - "+self.status_claim
    class Meta:
        verbose_name_plural = ('01. Danh sách yêu cầu')