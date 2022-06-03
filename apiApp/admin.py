from django.contrib import admin
from django.db.models import CharField
from django.db.models.functions import Length
# Register your models here.
CharField.register_lookup(Length, 'length')