from django import forms
from .models import Property, PropertyReview


class AddPropertyForm(forms.ModelForm):
    
    available_from = forms.DateField(widget=forms.TextInput(
        attrs={
            'type':'date'
        })
    )
    class Meta:
        model = Property
        fields = ('property_name', 'address', 'description', 'available_from', 'building_size', 'images', 'is_active')
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddPropertyForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].label = "Live"

    def save(self, request):
        property_obj = Property(**self.cleaned_data)
        property_obj.owner = request.user
        property_obj.save()
        return property_obj


class EditPropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = ('property_name', 'address', 'description', 'available_from', 'building_size', 'images', 'is_active')
        
    
    def __init__(self, *args, **kwargs):
        super(EditPropertyForm, self).__init__(*args, **kwargs)


class PropertyReviewForm(forms.ModelForm):

    class Meta:
        model = PropertyReview
        fields = ('property', 'review')
        
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PropertyReviewForm, self).__init__(*args, **kwargs)
    
    def save(self):
        property_review = PropertyReview(**self.cleaned_data)
        property_review.user = self.user
        property_review.save()
        return property_review