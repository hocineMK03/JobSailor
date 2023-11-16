from django.contrib import admin
from .models import Theuser,Theuser_worker,Theuser_Company,Session_model,Job_listing,Job_Category,Theuser_skills,Theuser_conversation,Theuser_messages,Theuser_notifications,Theuser_notifications_type,Job_accepted,Job_pending,Tokenhandlin
# Register your models here.

admin.site.register(Theuser)
admin.site.register(Theuser_worker)
admin.site.register(Theuser_Company)
admin.site.register(Session_model)
admin.site.register(Job_listing)
admin.site.register(Job_Category)
admin.site.register(Theuser_skills)
admin.site.register(Theuser_conversation)
admin.site.register(Theuser_messages)
admin.site.register(Theuser_notifications)
admin.site.register(Theuser_notifications_type)
admin.site.register(Job_accepted)
admin.site.register(Job_pending)
admin.site.register(Tokenhandlin)
