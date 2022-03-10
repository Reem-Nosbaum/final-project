class PasswordTooShort(Exception):

    def __init__(self, massage="Password Too Short"):
        self.massage = massage
        super().__init__(self.massage)

    def __str__(self):
        return self.massage

