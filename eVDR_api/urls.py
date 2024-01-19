from django.urls import path
from .views import status
from .views import handlers
from .views import users
from .views import indizio

urlpatterns = [
    path('status/ready', status.ready, name='ready'),
    path('bot/indizio', handlers.indizio, name='indizio'),
    path('bot/conversation', handlers.conversation, name='conversation'),
    path('bot/auth', handlers.auth, name='auth'),
    path('bot/reset_chat_table', handlers.reset_chat_table, name='reset_chat_table'),
    path('users/chat_ids', users.chat_ids, name='chat_ids'),
    path('users/chat_messages', users.chat_messages, name='chat_messages'),
    path('users/upload_phone_numbers', users.upload_phone_numbers, name='upload_phone_numbers'),
    path('indizio/create_indizio', indizio.create_indizio, name='create_indizio'),
]
