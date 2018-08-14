from django.conf.urls import url
from authentication import views

urlpatterns = [
        url(r'^login/$', views.UserLoginView.as_view(), name='login'),
        url(r'^register/$', views.RegisterView.as_view(), name='registration'),
]