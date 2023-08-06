import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import DoctorSpecialties


class BindDoctorSpecialtie:

    def __init__(self):
        self._doctor_id = ''
        self._specialty = 'pediatrician'

    def with_doctor(self, doctor):
        self._doctor_id = doctor.get('id')
        return self

    def with_specialty(self, spec):
        self._specialty = spec
        return self

    def generate(self):
        doc_spec = DoctorSpecialties(doctor_id=self._doctor_id,
                                     specialty=self._specialty,
                                     created_at=datetime.datetime.now(),
                                     updated_at=datetime.datetime.now())
        doc_spec.save()
        return model_to_dict(doc_spec)
