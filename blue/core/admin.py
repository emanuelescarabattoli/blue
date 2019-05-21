from django.contrib import admin

from .models import Register, RegisterRow, Statistics, StatisticsRowRegister, StatisticsRowStatistics


admin.site.register(Register)
admin.site.register(RegisterRow)
admin.site.register(Statistics)
admin.site.register(StatisticsRowRegister)
admin.site.register(StatisticsRowStatistics)
