from django.shortcuts import get_object_or_404, render

from .models import Patient
from .models import MedicalHistory
from .models import HPI
from .models import VitalSign
from .models import Diagnoses
from .models import PatientIntake

import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


from django.db.models import Max


def index(request):
    # return HttpResponse("Blah blah blah")
    return render(request,'index.html')



def patients(request):
    
    patients = Patient.objects.prefetch_related('medical_histories').all()
    return render(request,'patient.html', {'patients': patients})


def createPatient(request):
    if request.method == "POST":
        data = request.POST

       
        latest_card = Patient.objects.aggregate(Max('card_number'))['card_number__max']

        if latest_card and latest_card.isdigit():
            new_card_number = str(int(latest_card) + 1).zfill(4)
        else:
            new_card_number = "0001" 

        
        patient = Patient.objects.create(
            card_number=new_card_number,
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            grandfather_name=data.get("grandfather_name"),
            gender=data.get("gender"),
            date_of_birth=data.get("date_of_birth"),
            phone_number=data.get("phone_number"),
            nationality=data.get("nationality")
        )

        return JsonResponse({"status": "success", "id": patient.patient_id})

    return JsonResponse({"error": "Invalid method"}, status=400)

 
def updatePatient(request, patient_id):
    if request.method == "POST":
        patient = get_object_or_404(Patient, patient_id=patient_id)
        data = request.POST
        patient.first_name = data.get("first_name")
        patient.last_name = data.get("last_name")
        patient.grandfather_name = data.get("grandfather_name")
        patient.gender = data.get("gender")
        patient.date_of_birth = data.get("date_of_birth")
        patient.phone_number = data.get("phone_number")
        patient.nationality = data.get("nationality")
        patient.save()
        return JsonResponse({"status": "updated"})
    return JsonResponse({"error": "Invalid method"}, status=400)


def deletePatient(request, patient_id):
    if request.method == "POST":
        patient = get_object_or_404(Patient, patient_id=patient_id)
        patient.delete()
        return JsonResponse({"status": "deleted"})
    return JsonResponse({"error": "Invalid method"}, status=400)
    
     



def createMedicalRecord(request):
    if request.method == "POST":
        patient_id = request.POST.get('patientId') 
        
        try:
            patient = Patient.objects.get(patient_id=patient_id)  
        except Patient.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Patient not found"}, status=404)

        
        medical_history = MedicalHistory(
            patient=patient,
            status=MedicalHistory.MedicalHistoryStatus.PENDING,
        )
        
        medical_history.save()  

        return JsonResponse({"status": "Success", "message": "Medical History added"})
    
    return JsonResponse({"status": "Error", "message": "Invalid request method"}, status=405)



def medicalHistoryDetail(request):
    medical_history_id = request.GET.get("medicalHistoryId")
    medicalHistory = MedicalHistory.objects.get(medical_history_id = medical_history_id)
    return render(request,'medicalHistoryDetail.html', {'medicalHistoryDetail': medicalHistory})



def createHPI(request):
    if request.method == "POST":
        medical_history_id = request.POST.get('medicalHistoryId') 
        
        try:
            medical_history = MedicalHistory.objects.get(medical_history_id = medical_history_id)  
        except Patient.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Patient not found"}, status=404)
        
      
        chief_complaint = request.POST.get('chiefComplaint')
        severity = request.POST.get('severity')
        duration = request.POST.get('duration')
        location = request.POST.get('location', '')
        radiation = request.POST.get('radiation', '')
        quality = request.POST.get('quality', '')
        associated_symptoms = request.POST.get('associatedSymptoms', '')
        aggravating_factors = request.POST.get('aggravatingFactors', '')
        relieving_factors = request.POST.get('relievingFactors', '')
        previous_treatments = request.POST.get('previousTreatments', '')
        additional_notes = request.POST.get('additionalNotes', '')
        
        hpi = HPI(
            medical_history = medical_history,
            chief_complaint=chief_complaint,
            severity=severity,
            duration=duration,
            location=location,
            radiation=radiation,
            quality=quality,
            associated_symptoms=associated_symptoms,
            aggravating_factors=aggravating_factors,
            relieving_factors=relieving_factors,
            previous_treatments=previous_treatments,
            additional_notes=additional_notes
        )
        
        hpi.save()

        return JsonResponse({"status": "Success", "message": "HPI added"})
    
    return JsonResponse({"status": "Error", "message": "Invalid request method"}, status=405)



def createPatientIntake(request):
    if request.method == "POST":
        medical_history_id = request.POST.get('medicalHistoryId') 
        
        try:
            medical_history = MedicalHistory.objects.get(medical_history_id = medical_history_id)    
        except Patient.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Patient not found"}, status=404)
        
        marital_status = request.POST.get('maritalStatus')
        smoking_status = request.POST.get('smokingStatus')
        alcohol_use = request.POST.get('alcoholUse')
        drug_use = request.POST.get('drugUse')
        occupation = request.POST.get('occupation')
        family_history = request.POST.get('familyHistory', '')
        social_history = request.POST.get('socialHistory', '')
        allergies = request.POST.get('allergies', '')
        immunization_history = request.POST.get('immunizationHistory', '')
        previous_medical_procedures = request.POST.get('previousMedicalProcedures', '')
        current_medications = request.POST.get('currentMedications', '')
        additional_notes = request.POST.get('additionalNotes', '')
        
        intake_form = PatientIntake(
            medical_history = medical_history,
            marital_status=marital_status,
            smoking_status=smoking_status,
            alcohol_use=alcohol_use,
            drug_use=drug_use,
            occupation=occupation,
            family_history=family_history,
            social_history=social_history,
            allergies=allergies,
            immunization_history=immunization_history,
            previous_medical_procedures=previous_medical_procedures,
            current_medications=current_medications,
            additional_notes=additional_notes
        )
        
        intake_form.save()

        return JsonResponse({"status": "Success", "message": "Patient Intake added"})
    
    return JsonResponse({"status": "Error", "message": "Invalid request method"}, status=405)




def createDiagnoses(request):
    if request.method == "POST":
        medical_history_id = request.POST.get('medicalHistoryId') 
        
        try:
         medical_history = MedicalHistory.objects.get(medical_history_id = medical_history_id)  
        except Patient.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Patient not found"}, status=404)
        
        diagnosis_code = request.POST.get('diagnosisCode')
        diagnosis_name = request.POST.get('diagnosisName')
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        diagnosis = Diagnoses(
            medical_history = medical_history,
            diagnosis_code=diagnosis_code,
            diagnosis_name=diagnosis_name,
            status=status,
            notes=notes
        )
        
        diagnosis.save()

        return JsonResponse({"status": "Success", "message": "Diagnosis added"})
    
    return JsonResponse({"status": "Error", "message": "Invalid request method"}, status=405)



def createVitalSign(request):
    if request.method == "POST":
        medical_history_id = request.POST.get('medicalHistoryId') 
        
        try:
            medical_history = MedicalHistory.objects.get(medical_history_id = medical_history_id)  
        except Patient.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Patient not found"}, status=404)
        
        blood_pressure_systolic = request.POST.get('bloodPressureSystolic')
        blood_pressure_diastolic = request.POST.get('bloodPressureDiastolic')
        heart_rate = request.POST.get('heartRate')
        respiratory_rate = request.POST.get('respiratoryRate')
        temperature = request.POST.get('temperature')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        oxygen_saturation = request.POST.get('oxygenSaturation')
        
        vital_sign = VitalSign(
            medical_history = medical_history,
            blood_pressure_systolic=blood_pressure_systolic,
            blood_pressure_diastolic=blood_pressure_diastolic,
            heart_rate=heart_rate,
            respiratory_rate=respiratory_rate,
            temperature=temperature,
            weight=weight,
            height=height,
            oxygen_saturation=oxygen_saturation
        )
        
        vital_sign.save()

        return JsonResponse({"status": "Success", "message": "Vital Signs added"})
    
    return JsonResponse({"status": "Error", "message": "Invalid request method"}, status=405)

