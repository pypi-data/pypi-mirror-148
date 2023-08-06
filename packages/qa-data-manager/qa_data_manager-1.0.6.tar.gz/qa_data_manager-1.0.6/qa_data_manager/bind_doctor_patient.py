import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import DoctorPatient


class BindDoctorPatient:

    def __init__(self):
        self._doctor_id = ''
        self._patient_id = ''
        self._created_at = datetime.datetime.now()
        self._updated_at = datetime.datetime.now()

    def with_doctor(self, doctor):
        self._doctor_id = doctor.get('id')
        return self

    def with_patient(self, patient):
        self._patient_id = patient.get('id')
        return self

    def generate(self):
        doctor_patient = DoctorPatient(confirm_appointment=0,
                                       created_at=self._created_at,
                                       doctor=self._doctor_id,
                                       doctor_new=1,
                                       message='hello user',
                                       patient=self._patient_id,
                                       patient_new=1,
                                       source='admin',
                                       updated_at=self._updated_at)
        doctor_patient.save()
        return model_to_dict(doctor_patient)
