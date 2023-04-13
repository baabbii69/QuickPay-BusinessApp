from django.contrib import admin
from .models import *


admin.site.register((Industry, Incorporation, States, BusnessAdress, IdDocument, PesonalAdderss, DedicatedPerson, VerifyBusiness))
