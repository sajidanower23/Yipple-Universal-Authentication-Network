import os
import json
import bcrypt
import uuid

class KomradeConfig:
    def __init__(self, name):
        self.config_file = os.path.join(os.path.dirname(__file__), "../" + name + ".json")

        if not os.path.exists(self.config_file):
            open(self.config_file, "w").write("{}")

    def read(self):
        return json.loads(open(self.config_file, "r").read())

    def write(self, data):
        with open(self.config_file, 'w') as fh:
            fh.write(json.dumps(data))

def sanitise_name(name):
    return name.replace("/", "")

def user_exists(komrade):
    # try:
    return komrade.read() != {}
    # return True
    # except FileNotFoundError:
    #     return False

def registerUser(username, password):
    # @todo: security hole. sanitize ``username``!
    username = sanitise_name(username)
    komrade = KomradeConfig(username)
    # sanitize here!
    data = {
        'username': username,
        'password': password # @todo hash this password
    }
    if user_exists(komrade):
        return False
    komrade.write(data)
    return True

def validateUser(username, password):
    komrade = KomradeConfig(username)
    # Implement me

    data = komrade.read()
    # @todo Check the hashes of these passwords!
    return data['password'] == password
