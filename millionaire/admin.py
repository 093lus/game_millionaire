from django.contrib import admin
from millionaire.models import Question, Choice, UserBestScore

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserBestScore)
