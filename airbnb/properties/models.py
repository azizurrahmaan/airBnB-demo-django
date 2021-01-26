from db.models import BaseModel
from address.models import AddressField
from autoslug import AutoSlugField
from datetime import datetime
from autoslug import AutoSlugField
# from django.contrib.postgres.fields import ArrayField
from django_better_admin_arrayfield.models.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User

def get_slug(instance):
    return f'{instance.address}-{instance.id}'.lower().replace(' ', '-')


class Property(BaseModel):
    owner = models.ForeignKey(
        User,
        related_name='properties',
        help_text="Property's owner.",
        on_delete=models.CASCADE
    )

    slug = AutoSlugField(
        populate_from=get_slug,
        unique=True,
        editable=True,
        null=True,
        blank=True
    )

    property_name = models.CharField(
        blank=True,
        null=True,
        max_length=255
    )
   
    address =models.CharField(max_length=255,default="")

    
    features = ArrayField(
        models.CharField(max_length=100),
        verbose_name="Key Features",
        help_text="Key features for this property",
        default=list,
        blank=True
    )

    description = models.TextField()

    available_from = models.DateField(
        blank=True,
        null=True,
        default=None
    )

    building_size = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True
    )

    availability = models.IntegerField(
        null=True,
        blank=True
    )

    images = models.FileField(
        upload_to='properties/images',
        blank=True,
        null=True
    )


    def __str__(self):
        return f'{self.id} : {self.address}'


    def get_available_now(self):
        return self.available_from <= datetime.today().date() if self.available_from else True

    def get_days_available(self):
        return (datetime.today().date() - self.created_on.date()).days


    def get_address(self):
        addy = self.address
        if addy and addy.formatted:
            return addy.formatted
        if addy and addy.raw:
            return addy.raw
        return ""

    def save(self, *args, **kwargs):
        self.slug = get_slug(self)
        super(Property, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created_on',)

