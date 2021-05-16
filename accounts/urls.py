from django.urls import path, include
app_name = 'acounts'

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('signup/', include('dj_rest_auth.registration.urls')),
]
