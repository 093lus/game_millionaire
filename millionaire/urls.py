from django.conf.urls import url
from millionaire import views

urlpatterns = [
        url(r'^$', views.Game.as_view(), name='index'),
        url(r'^finish/(?P<score>[^/]+)/?$', views.GameFinishView.as_view(), name='finish'),
        url(r'^question/$', views.QuestionView.as_view(), name='question'),
]