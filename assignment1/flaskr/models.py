import os
import json
import bcrypt
import uuid

class KomradeConfig:
    def __init__(self, name):
        name = sanitise_name(name)
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
    return komrade.read() != {}

def registerUser(username, password):
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

# Implement me
def validateUser(username, password):
    komrade = KomradeConfig(username)
    data = komrade.read()
    # @todo Check the hashes of these passwords!
    return user_exists(komrade) and data['password'] == password
