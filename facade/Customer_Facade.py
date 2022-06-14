from errors.Invalid_Input import Invalid_Input
from errors.error_flight_not_found import FlightNotFound
from errors.error_ticket_not_found import TicketNotFound
from facade.FacadeBase import FacadeBase
from errors.Invalid_Toke import InvalidToken
from tables.Customers import Customers
from db_files.logger import Logger
from tables.Tickets import Tickets
from tables.Flights import Flights
from errors.error_no_more_tickets import NoMoreTickets
from LoginToken import LoginToken


class CustomerFacade(FacadeBase):

    def __init__(self, repo):
        super().__init__(repo)
        self.logger = Logger.get_instance()
        self.LoginToken = LoginToken

    def update_customer(self, customer, customer_id, token):
        if not self.check_token(Customers, token):
            raise InvalidToken
        self.logger.logger.debug('updating customer ...')
        if not isinstance(customer_id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input
        else:
            self.repo.update_by_id(Customers, Customers.id, customer_id, customer)
            self.logger.logger.info('customer updated!')

    def add_ticket(self, ticket, token):
        if not self.check_token(Customers, token):
            raise InvalidToken
        self.logger.logger.debug('adding ticket ...')
        if not isinstance(ticket, Tickets):
            self.logger.logger.error('Input must be an "Tickets" object!')
            raise Invalid_Input('Input must be an "Tickets" object!')
        flight = self.get_flight_by_id(ticket.flight_id)
        if flight is None:
            self.logger.logger.error(f'{FlightNotFound} - Flight #{ticket.flight_id} was not found!')
            raise FlightNotFound
        elif flight.remaining_tickets == 0:
            self.logger.logger.error(f'{NoMoreTickets} - No seats available. Ticket canceled!')
            raise NoMoreTickets
        else:
            self.repo.add(ticket)
            self.repo.update_by_id(Flights, Flights.id, ticket.flight_id,
                                   {'remaining_tickets': flight.remaining_tickets - 1})
            self.logger.logger.info(f'Ticket created!')

    def remove_ticket(self, ticket, token):
        if not self.check_token(Customers, token):
            raise InvalidToken
        self.logger.logger.debug('removing ticket ...')
        if not isinstance(ticket, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input
        if self.repo.get_by_id(Tickets, ticket) is None:
            self.logger.logger.error(f'{TicketNotFound} - Ticket was not found!')
            raise TicketNotFound
        else:
            self.repo.delete_by_id(Tickets, Tickets.id, ticket)
            self.logger.logger.info('ticket  Deleted!')

    def get_ticket_by_customer(self, customer, token):
        if not self.check_token(Customers, token):
            raise InvalidToken
        self.logger.logger.debug('looking for ticket...')
        if not isinstance(customer, int):
            self.logger.logger.error('Input must be an integer!!')
            raise Invalid_Input
        else:
            self.logger.logger.info('Ticket for customer shown!')
            return self.repo.get_by_column_value(Tickets, Tickets.customer_id, customer)

    def get_my_tickets(self):
        pass

    def __str__(self):
        return f'{super().__init__}'
