from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^(?P<id>\d+)', views.bot_question, name='question'),
    url(r'^/answer/(?P<id>\d+)', views.answer_bot, name='answer'),
]
