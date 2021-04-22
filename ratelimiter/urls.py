from django.urls import path

from .views import rate_limiting

urlpatterns = [
    path('', rate_limiting),
]
