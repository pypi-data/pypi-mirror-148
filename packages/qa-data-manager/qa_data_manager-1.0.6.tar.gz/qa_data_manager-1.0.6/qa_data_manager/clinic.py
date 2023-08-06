from faker import Faker

from qa_data_manager.data_base_model import Clinics


class GenerateClinic:
    __fake = Faker('ru_RU')

    def create(self):
        clinic = Clinics(avatar=self.__fake.image_url(),
                         city=self.__fake.city(),
                         created_at=self.__fake.date(pattern="%Y-%m-%d %H:%M:%S", end_datetime=None),
                         description=self.__fake.address() + '__t1e1s1t__',
                         email=self.__fake.email(),
                         is_demo=False,
                         name=self.__fake.profile()['company'],
                         phone=self.__fake.phone_number(),
                         public_token='$2y$11$aKqz0W7AGox5SL4/vzChxOzoCFy.bx628U44m.cNhZLeh8umwadYK',
                         rate=0.00,
                         site=self.__fake.hostname(),
                         street=self.__fake.address(),
                         type='default',
                         updated_at=self.__fake.date(pattern="%Y-%m-%d %H:%M:%S", end_datetime=None))
        clinic.save()
        return clinic
