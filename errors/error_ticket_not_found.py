class TicketNotFound(Exception):

    def __init__(self, massage="Ticket Not Found"):
        self.massage = massage
        super().__init__(self.massage)

    def __str__(self):
        return self.massage
