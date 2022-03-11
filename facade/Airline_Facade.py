import LoginToken
from errors.Invalid_Input import Invalid_Input
from errors.Invalid_Toke import InvalidToken
from errors.error_airline_not_found import AirlineNotFound
from errors.error_flight_not_found import FlightNotFound
from facade.FacadeBase import FacadeBase
from tabels.Airline_Companies import Airline_Companies
from tabels.Flights import Flights
from logger import Logger
from LoginToken import LoginToken


class AirlineFacade(FacadeBase):

    def __init__(self, repo):
        super().__init__(repo)
        self.logger = Logger.get_instance()
        self.login_token = LoginToken

    def get_flights_by_airline(self, airline, token):
        self.logger.logger.debug(f'Attempting to fetch flight(s) for airline #{airline}...')
        if not isinstance(airline, int):
            self.logger.logger.error(f'{Invalid_Input} - Input must be an integer!!')
            raise Invalid_Input('Input must be an integer!')
        elif self.repo.get_by_id(Airline_Companies, airline) is None:
            self.logger.logger.error(f'{AirlineNotFound} - Airline #{airline} was not found!')
            raise AirlineNotFound
        else:
            if not self.check_token(Airline_Companies, token):
                self.logger.logger.error(f'{InvalidToken} - you cannot edit for other airline!')
                raise InvalidToken
            else:
                self.logger.logger.info(f'Flight(s) for #{airline} Displayed!')
                return self.repo.get_by_column_value(Flights, Flights.airline_company_id, airline)

    def update_airline(self, airline, airline_id, token):
        if not self.check_token(Airline_Companies, token):
            raise InvalidToken
        self.logger.logger.debug('updating airline ...')
        if not isinstance(airline_id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        elif not isinstance(airline, dict):
            self.logger.logger.error('Input must be a dictionary!')
            raise Invalid_Input('Input must be an dictionary!')
        else:
            self.repo.update_by_id(Airline_Companies, Airline_Companies.id, airline_id, airline)
            self.logger.logger.info('airline updated!')

    def add_flight(self, flight, token):
        if not self.check_token(Airline_Companies, token):
            raise InvalidToken
        self.logger.logger.debug('adding flight ...')
        if not isinstance(flight, Flights):
            self.logger.logger.error('Input must be an "Flights" object!')
            raise Invalid_Input('Input must be an "Flights" object!')
        elif flight.remaining_tickets < 0:
            self.logger.logger.error('Negative number of seats is impossible!')
        elif flight.origin_country_id is flight.destination_country_id:
            self.logger.logger.error('origin country and destination country cannot be the same..')
        else:
            self.repo.add(flight)
            self.logger.logger.info('Flight created!')

    def update_flight(self, flight, flight_id, token):
        if not self.check_token(Airline_Companies, token):
            self.logger.logger.debug('updating flight ...')
            raise InvalidToken
        if not isinstance(flight_id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        elif not isinstance(flight, dict):
            self.logger.logger.error('Input must be a dictionary!')
            raise Invalid_Input('Input must be an dictionary!')
        elif self.get_flight_by_id(flight_id) is None:
            self.logger.logger.error(f'{FlightNotFound} - Flight #{flight_id} was not found!')
            raise FlightNotFound
        else:
            self.repo.update_by_id(Flights, Flights.id, flight_id, flight)
            self.logger.logger.info('flight updated!')

    def remove_flight(self, flight_id, token):
        if not self.check_token(Airline_Companies, token):
            self.logger.logger.debug('removing flight ...')
            raise InvalidToken
        if not isinstance(flight_id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        elif self.get_flight_by_id(flight_id) is None:
            self.logger.logger.error(f'{FlightNotFound} - Flight #{flight_id} was not found!')
            raise FlightNotFound
        else:
            all_flights = self.get_my_flights(token)
            for flight in all_flights:
                self.repo.delete_by_id(Flights, 'id', flight.id)
            self.repo.delete_by_id(Flights, Flights.id, flight_id)
            self.logger.logger.info('Flight  Deleted!')

    def get_my_flights(self, airline):
        return list(filter(lambda f : f.airline_company_id == airline.id, self.repo.get_all(Flights)))

    def __str__(self):
        return f'{super().__init__}'
