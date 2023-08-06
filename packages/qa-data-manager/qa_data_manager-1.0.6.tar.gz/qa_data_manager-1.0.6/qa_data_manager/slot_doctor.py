import datetime

from faker import Faker
from playhouse.shortcuts import model_to_dict


from qa_data_manager.data_base_model import SlotsDoctors


class GenerateSlotDoctor:
    __fake = Faker('ru_RU')
    __time_mask = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        self._type = 'both'
        self._doctor_id = ''
        self._start_at = datetime.datetime.now()
        self._end_at = ''
        self._duration = 1
        self._context = 'default'
        self._created_at = datetime.datetime.now()
        self._updated_at = datetime.datetime.now()
        self._deleted_at = None
        self._count = 1

    def with_admin_context(self):
        self._context = 'admin'
        return self

    def with_doctor_context(self):
        self._context = 'doctor'
        return self

    def with_integration_context(self):
        self._context = 'integration'
        return self

    def with_count(self, count):
        self._count = count
        return self

    def is_deleted(self):
        self._deleted_at = datetime.datetime.now()
        return self

    def with_doctor(self, doctor):
        self._doctor_id = doctor.get('id')
        return self

    def with_online_type(self):
        self._type = 'online'
        return self

    def with_offline_type(self):
        self._type = 'offline'
        return self

    def with_duration(self, duration):
        self._duration = duration
        self._end_at = self._start_at + datetime.timedelta(minutes=int(self._duration))
        return self

    def generate(self):
        i = 1
        list_slot_ids = []
        while (i <= self._count):
            slot_doctor = SlotsDoctors(doctor_id=self._doctor_id,
                                type=self._type,
                                start_at=self._start_at,
                                duration=self._duration,
                                end_at=self._end_at,
                                context=self._context,
                                created_at=self._created_at,
                                updated_at=self._updated_at)
            slot_doctor.save()
            slot_id = model_to_dict(slot_doctor.get('id'))
            list_slot_ids.append(slot_id)
            i = i + 1
            self._start_at = self._end_at
            self._end_at = self._start_at + datetime.timedelta(minutes=int(self._duration))

        return list_slot_ids
