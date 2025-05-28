from django.db import models

from django.db import models
from django.utils import timezone


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    card_number = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=255, blank=True, null=True)
    passport_path = models.CharField(max_length=255, blank=True, null=True)
    grandfather_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=100, blank=True, null=True)

    class MaritalStatus(models.TextChoices):
        SINGLE = 'SINGLE', 'Single'
        MARRIED = 'MARRIED', 'Married'
        DIVORCED = 'DIVORCED', 'Divorced'
        WIDOWED = 'WIDOWED', 'Widowed'
    marital_status = models.CharField(max_length=20, choices=MaritalStatus.choices, null=True, blank=True)

    profession = models.CharField(max_length=100, blank=True, null=True)
    traveling_to = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    zone = models.CharField(max_length=100, blank=True, null=True)
    woreda = models.CharField(max_length=100, blank=True, null=True)
    house_number = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    user_profile_image = models.CharField(max_length=255, blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()

    allergies = models.TextField(blank=True, null=True)
    chronic_illness = models.TextField(blank=True, null=True)
    medication = models.TextField(blank=True, null=True)
    
   

    class PatientStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        DECEASED = 'DECEASED', 'Deceased'
    patient_status = models.CharField(max_length=20, choices=PatientStatus.choices)

   
    phone_number = models.CharField(max_length=20, blank=True, null=True)
  
    organization_id = models.IntegerField(null=True, blank=True)
    branch_id = models.IntegerField(null=True, blank=True)
    is_credit_customer = models.BooleanField(default=False)





class MedicalHistory(models.Model):
    medical_history_id = models.AutoField(primary_key=True)

    # Foreign key to Patient 
    patient = models.ForeignKey(
        'Patient',
        to_field='patient_id',
        on_delete=models.CASCADE,
        related_name='medical_histories'
    )

   
    family_member_id = models.IntegerField(null=True, blank=True)

   


    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    medical_history_multiple_session_id = models.IntegerField(null=True, blank=True)

    class MedicalHistoryStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    status = models.CharField(max_length=20, choices=MedicalHistoryStatus.choices)


    organization_id = models.IntegerField(null=True, blank=True)

    reason_for_change = models.TextField(blank=True, null=True)
    odoo_order_id = models.CharField(max_length=255, blank=True, null=True)
    default_code_odoo = models.CharField(max_length=255, blank=True, null=True)
    odoo_order_line_id = models.CharField(max_length=255, blank=True, null=True)



class HPI(models.Model):
    medical_History = models.ForeignKey('MedicalHistory', on_delete=models.CASCADE, related_name='hpis')
    date_created = models.DateTimeField(default=timezone.now)
    chief_complaint = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)
    duration = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    radiation = models.CharField(max_length=100, blank=True, null=True)
    quality = models.CharField(max_length=255, blank=True, null=True)
    associated_symptoms = models.TextField(blank=True, null=True)
    aggravating_factors = models.TextField(blank=True, null=True)
    relieving_factors = models.TextField(blank=True, null=True)
    previous_treatments = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"HPI for {self.patient.name} - {self.chief_complaint}"


class PatientIntake(models.Model):
    medical_History = models.ForeignKey('MedicalHistory', on_delete=models.CASCADE, related_name='patient_intakes')
    date_created = models.DateTimeField(default=timezone.now)
    marital_status = models.CharField(max_length=50, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')])
    smoking_status = models.CharField(max_length=50, choices=[('Never', 'Never'), ('Former', 'Former'), ('Current', 'Current')])
    alcohol_use = models.CharField(max_length=50, choices=[('Never', 'Never'), ('Occasional', 'Occasional'), ('Frequent', 'Frequent')])
    drug_use = models.CharField(max_length=50, choices=[('Never', 'Never'), ('Occasional', 'Occasional'), ('Frequent', 'Frequent')])
    occupation = models.CharField(max_length=255)
    family_history = models.TextField(blank=True, null=True)
    social_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    immunization_history = models.TextField(blank=True, null=True)
    previous_medical_procedures = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Patient Intake Form for {self.patient.name}"

# Model for Diagnoses
class Diagnoses(models.Model):
    medical_History = models.ForeignKey('MedicalHistory', on_delete=models.CASCADE, related_name='diagnoses')
    diagnosis_code = models.CharField(max_length=50)
    diagnosis_name = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Resolved', 'Resolved'), ('Chronic', 'Chronic')])
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.diagnosis_name} - {self.patient.name}"

# Model for Vital Signs
class VitalSign(models.Model):
    medical_History = models.ForeignKey('MedicalHistory', on_delete=models.CASCADE, related_name='vital_signs')
    date_created = models.DateTimeField(default=timezone.now)
    blood_pressure_systolic = models.IntegerField()
    blood_pressure_diastolic = models.IntegerField()
    heart_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    temperature = models.FloatField()
    weight = models.FloatField()
    height = models.FloatField()
    oxygen_saturation = models.FloatField()

    def __str__(self):
        return f"Vital Signs for {self.patient.name} - {self.date_recorded}"
