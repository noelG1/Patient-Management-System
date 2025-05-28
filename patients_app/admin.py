from django.contrib import admin

from .models import Patient
from .models import MedicalHistory
from .models import HPI
from .models import VitalSign
from .models import Diagnoses
from .models import PatientIntake

admin.site.register(Patient)
admin.site.register(MedicalHistory)
admin.site.register(HPI)
admin.site.register(VitalSign)
admin.site.register(Diagnoses)
admin.site.register(PatientIntake)
