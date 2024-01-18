from django.contrib import admin
from .models import Chat, AuthorizedPhoneNumber, Indizi

# Register your models here.
admin.site.register(Chat)
admin.site.register(AuthorizedPhoneNumber)
admin.site.register(Indizi)
