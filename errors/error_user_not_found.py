class UserNotFound(Exception):

    def __init__(self, massage="User Not Found"):
        self.massage = massage
        super().__init__(self.massage)

    def __str__(self):
        return self.massage
