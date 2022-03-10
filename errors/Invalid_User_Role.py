class InvalidUserRole(Exception):

    def __init__(self, massage="Invalid User Role"):
        self.massage = massage
        super().__init__(self.massage)

    def __str__(self):
        return self.massage
