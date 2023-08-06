from qa_data_manager.jwt_clinic_token import Jwt_clinic_toket


class GenerateClinicToken:

    def get_token(self, client_key, client_secret):
        return Jwt_clinic_toket(client_key, client_secret).get()
