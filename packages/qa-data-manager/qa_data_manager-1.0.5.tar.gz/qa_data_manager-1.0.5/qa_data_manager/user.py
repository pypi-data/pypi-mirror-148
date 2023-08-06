import datetime as mytime

from faker import Faker
from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import Users
from qa_data_manager.bind_clinic_user import BindClinicUser


class GenerateUser:
    fake = Faker('ru_RU')

    def __init__(self):
        self._type = 'doctor'
        self._self_appointment = 0
        self._has_primary_acceptance = 0
        self._activatied_at = None
        self._deleted_at = None
        self._type_chat = 'free'
        self._clinic = 14
        self._is_showcase = 1

    def patient(self):
        self._type = 'patient'
        return self

    def doctor(self):
        self._type = 'doctor'
        return self

    def with_self_appointment(self):
        self._self_appointment = 1
        return self

    def with_primary_acceptance(self):
        self._has_primary_acceptance = 1
        return self

    def with_paid_chat(self):
        self._type_chat = 'paid'
        return self

    def is_showcase_false(self):
        self._is_showcase = 0
        return self

    def is_activated(self):
        self._activatied_at = mytime.datetime.now()
        return self

    def is_deleted(self):
        self._deleted_at = mytime.datetime.now()
        return self

    def with_clinic(self, clinic):
        self._clinic = clinic
        return self

    def generate(self):
        user = Users(activated_at=self._activatied_at,
                     avatar=self.fake.image_url(width=None, height=None),
                     created_at=mytime.datetime.now(),
                     date_of_birth=self.fake.date(pattern="%Y-%m-%d", end_datetime=None),
                     email=self.fake.email(),
                     full_name=self.fake.name(),
                     gender='male',
                     has_primary_acceptance=self._has_primary_acceptance,
                     hash="XRJI",
                     is_showcase=self._is_showcase,
                     is_test=0,
                     password="$2y$12$F02YDfRJLKD/nuNVhIefY.Ux1lkbd8jYdNmtH3c22F/o/8eQNZwzO",
                     phone=self.fake.numerify(text='+%%%%%%%%%%%'),
                     remember_token="blUSTapXajDs1BNFfLOKPrSumVExvthjaE80cP9qqZpA6l54b7vwKXkqbg6W",
                     save_video_at=0,
                     self_appointment=self._self_appointment,
                     send_email=1,
                     send_sms=1,
                     silence_activated_at=0,
                     source='admin',
                     type=self._type,
                     type_chat=self._type_chat,
                     updated_at=mytime.datetime.now(),
                     deleted_at=self._deleted_at)
        user.save()
        BindClinicUser().with_user(model_to_dict(user)).with_clinic(self._clinic).generate()
        return model_to_dict(user)
