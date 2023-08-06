from qa_data_manager.bind_clinic_user import BindClinicUser
from qa_data_manager.bind_doctor_patient import BindDoctorPatient
from qa_data_manager.chat import GenerateChat
from qa_data_manager.data_base_model import database
from qa_data_manager.service import GenerateService
from qa_data_manager.user import GenerateUser
from qa_data_manager.slot_doctor import GenerateSlotDoctor
from qa_data_manager.clinic import GenerateClinic
from qa_data_manager.bind_doctor_specialtie import BindDoctorSpecialtie
from qa_data_manager.user_token import GenerateUserToken
from qa_data_manager.clinic_token import GenerateClinicToken


from config import Config as cfg


class DataGenerator:

    @staticmethod
    def db_connection(db_host, db_name, db_port, user_name, user_password, base_url):
        database.init(db_name, host=db_host, port=db_port, user=user_name, password=user_password)
        cfg.url = base_url

    generate_user = GenerateUser()
    bind_clinic_user = BindClinicUser()
    bind_doctor_patient = BindDoctorPatient()
    generate_service = GenerateService()
    generate_chat = GenerateChat()
    generate_slot_doctor = GenerateSlotDoctor()
    generate_clinic = GenerateClinic()
    bind_doctor_specialtie = BindDoctorSpecialtie()
    generate_user_token = GenerateUserToken()
    generate_clinic_token = GenerateClinicToken()

