from django.contrib import admin
from .models import *


admin.site.register(Project)
admin.site.register(Ticket)
admin.site.register(TicketHistory)
admin.site.register(Task)
admin.site.register(TaskHistory)
