import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import Chats


class GenerateChat:

    def __init__(self):
        self._doctor_id = ''
        self._patient_id = ''
        self._created_at = datetime.datetime.now()
        self._updated_at = datetime.datetime.now()
        self._last_chat_message = 1
        self._last_med_card_message = 1

    def with_doctor(self, doctor):
        self._doctor_id = doctor.get('id')
        return self

    def with_patient(self, patient):
        self._patient_id = patient.get('id')
        return self

    def generate(self):
        chat = Chats(doctor=self._doctor_id,
                     patient=self._patient_id,
                     created_at=self._created_at,
                     updated_at=self._updated_at)
        chat.save()
        return model_to_dict(chat)
