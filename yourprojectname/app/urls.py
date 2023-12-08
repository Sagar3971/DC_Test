from django.urls import path
from . import views

urlpatterns = [
    path('chatbot', views.chatbot),
    path('', views.chatbot),
    path('transcribe_audio/', views.transcribe_audio, name='transcribe_audio'),
]
