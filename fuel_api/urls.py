from django.urls import path
from .views import OptimizeRouteView

urlpatterns = [
    path('route/', OptimizeRouteView.as_view(), name='optimize-route'),
]