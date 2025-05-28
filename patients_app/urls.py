from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('patients/', views.patients, name='patients'),
    path('patients/create/', views.createPatient, name='create_patient'),
    path('patients/update/<int:id>/', views.updatePatient, name='update_patient'),
    path('patients/delete/<int:id>/', views.deletePatient, name='delete_patient'),

    path('medical-history/create/', views.createMedicalRecord, name='create_medical_history'),
    path('medical-history/detail/', views.medicalHistoryDetail, name='medical_history_detail'),

    path('hpi/create/', views.createHPI, name='create_hpi'),
    path('intake/create/', views.createPatientIntake, name='create_patient_intake'),
    path('diagnoses/create/', views.createDiagnoses, name='create_diagnoses'),
    path('vitals/create/', views.createVitalSign, name='create_vital_sign'),
]
