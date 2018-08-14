from django.conf.urls import url
from millionaire import views

urlpatterns = [
        url(r'^$', views.Game.as_view(), name='index'),
        url(r'^question/$', views.QuestionView.as_view(), name='question'),
]