from qa_data_manager.jwt_user_token import Jwt_user_toket


class GenerateUserToken:

    def get_token(self, user):
        return Jwt_user_toket(user).get()
