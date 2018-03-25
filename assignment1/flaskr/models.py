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

<<<<<<< HEAD
def sanitise_name(name):
    return name.replace("/", "")

def user_exists(komrade):
    return komrade.read() != {}
=======
def registerUser(username, password):
    komrade = KomradeConfig("user")

    user_store = komrade.read()
    if username in user_store:
        raise NameError("User already exists in database")

    pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_store[username] = pw_hash.decode('utf-8')

    komrade.write(user_store)
>>>>>>> 94156f038df3829a42e14084aaad6ac56ffd1f26

def registerUser(username, password):
    username = sanitise_name(username)
    komrade = KomradeConfig(username)
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
<<<<<<< HEAD
    komrade = KomradeConfig(username)
    data = komrade.read()
    # @todo Check the hashes of these passwords!
    return user_exists(komrade) and data['password'] == password
=======
    komrade = KomradeConfig("user")

    user_store = komrade.read()
    if not username in user_store:
        return False

    stored_pw = user_store[username].encode('utf-8')

    return bcrypt.hashpw(password.encode('utf-8'), stored_pw) == stored_pw 
>>>>>>> 94156f038df3829a42e14084aaad6ac56ffd1f26
