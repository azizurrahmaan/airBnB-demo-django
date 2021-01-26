from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from properties.views import Dashboard, MyProperties, AddProperty, Properties, EditProperty, PropertyDetail, add_property_review

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("properties/", Properties.as_view(), name="properties"),
    path("properties/my", MyProperties.as_view(), name="my_properties"),
    path("properties/add", AddProperty.as_view(), name="add_property"),
    path("properties/edit/<slug:slug>", EditProperty.as_view(), name="edit_property"),
    path("properties/detail/<slug:slug>", PropertyDetail.as_view(), name="detail_property"),
    path("properties/add_review", add_property_review, name="add_property_review"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)