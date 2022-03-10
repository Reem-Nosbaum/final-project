
class NoMoreTickets(Exception):

    def __init__(self, massage="No More Tickets left"):
        self.massage = massage
        super().__init__(self.massage)

    def __str__(self):
        return self.massage
