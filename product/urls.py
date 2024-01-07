from django.urls import path
from .views import GetTest, AllTest

urlpatterns = [
    path("api2/<int:pk>/", GetTest.as_view(), name="api2_RET"),
    path("api1/", AllTest.as_view(), name="api1_ALL"),
]