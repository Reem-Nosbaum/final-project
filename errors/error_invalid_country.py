class InvalidCountry(Exception):
    def __init__(self, message="Invalid country ID - Check again if it exists!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'InvalidCountry: {self.message}'