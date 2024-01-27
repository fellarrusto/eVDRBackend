from django.contrib import admin
from .models import Chat, AuthorizedPhoneNumber, Indizi, UserMessage, UserStats

# Register your models here.
admin.site.register(Chat)
admin.site.register(AuthorizedPhoneNumber)
admin.site.register(Indizi)
admin.site.register(UserMessage)
admin.site.register(UserStats)
