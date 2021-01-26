from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from properties.views import Dashboard, MyProperties, AddProperty, Properties, EditProperty, PropertyDetail

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("properties/", Properties.as_view(), name="properties"),
    path("properties/my", MyProperties.as_view(), name="my_properties"),
    path("properties/add", AddProperty.as_view(), name="add_property"),
    path("properties/edit/<int:pk>", EditProperty.as_view(), name="edit_property"),
    path("properties/detail/<int:pk>", PropertyDetail.as_view(), name="detail_property"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)