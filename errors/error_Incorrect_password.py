class IncorrectPassword(Exception):

    def __init__(self, massage="Incorrect password"):
        self.massage = massage
        super().__init__(self.massage)

    def __str__(self):
        return self.massage
