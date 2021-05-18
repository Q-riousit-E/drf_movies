from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('signup/', views.signup),
]
