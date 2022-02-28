from django.contrib import admin
import framework

# Register your models here.
from framework.models import Terminal, Locker, Technician, Product, Mission, Action

admin.site.register(Terminal)
admin.site.register(Locker)
admin.site.register(Technician)
admin.site.register(Product)
admin.site.register(Mission)
admin.site.register(Action)