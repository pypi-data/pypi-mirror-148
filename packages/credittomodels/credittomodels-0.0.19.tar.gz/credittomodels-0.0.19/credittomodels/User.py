

class User(object):

    def __init__(self, user_id: int, user_name: str, password: str, jwt_token: str,
                 key: str, token_creation_time: str, role_id: int):

        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.jwt_token = jwt_token
        self.key = key
        self.token_creation_time = token_creation_time
        self.role_if = role_id
