# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Proverb)
admin.site.register(Person)
admin.site.register(AnalysisInfo)
admin.site.register(AnalysisByAge)
admin.site.register(AnalysisByGender)
