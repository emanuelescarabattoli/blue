from django.contrib import admin

from .models import Register, Item, Statistics


admin.site.register(Register)
admin.site.register(Item)
admin.site.register(Statistics)
