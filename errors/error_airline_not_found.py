class AirlineNotFound(Exception):
    def __init__(self, message="Airline not found. Please check again!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'AirlineNotFound: {self.message}'
