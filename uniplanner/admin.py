from django.contrib import admin
from .models import User, event, module, usermodule,deadline, toask
# Register your models here.
admin.site.register(User)
admin.site.register(event)
admin.site.register(module)
admin.site.register(usermodule)
admin.site.register(toask)
admin.site.register(deadline)