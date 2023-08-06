import datetime

from qa_data_manager.data_base_model import ClinicUser


class BindClinicUser:

    def __init__(self):
        self._clinic_id = 14
        self._user_id = ''
        self._type = ''
        self._created_at = datetime.datetime.now()
        self._updated_at = datetime.datetime.now()

    def with_clinic(self, clinic_id):
        self._clinic_id = clinic_id
        return self

    def with_user(self, user):
        self._user_id = user.get('id')
        self._type = user.get('type')
        return self

    def generate(self):
        clinic_user = ClinicUser(clinic=self._clinic_id,
                                 created_at=self._created_at,
                                 type=self._type,
                                 updated_at=self._updated_at,
                                 user=self._user_id)
        clinic_user.save()
        return clinic_user
