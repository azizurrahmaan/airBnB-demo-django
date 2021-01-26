from django import forms
from .models import Property
# from django.contrib.postgres.forms import SimpleArrayField
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

class AddPropertyForm(forms.ModelForm):
    
    class Meta:
        model = Property
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddPropertyForm, self).__init__(*args, **kwargs)

    def save(self, request):
        property_obj = Property(self.cleaned_data)
        property_obj.owner = request.user
        property_obj.save()
        return property_obj