from django.urls import path, include
from properties.views import Dashboard, MyProperties, AddProperty

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("my-properties/", MyProperties.as_view(), name="my_properties"),
    path("add-property", AddProperty.as_view(), name="add_property"),
]