class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self):
        return "Id: {}, Username: {}, password {}".format(self.id, self.username, self.password)
