class Invalid_Input(Exception):

    def __init__(self, massage="Invalid input"):
        self.massage = massage
        super().__init__(self.massage)

    def __str__(self):
        return self.massage
