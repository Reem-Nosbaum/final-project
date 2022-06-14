from datetime import datetime

from sqlalchemy import Text

from errors.Invalid_Input import Invalid_Input
from errors.error_airline_not_found import AirlineNotFound
from errors.error_flight_not_found import FlightNotFound
from errors.error_invalid_country import InvalidCountry
from tables.Administrators import Administrators
from tables.Customers import Customers
from tables.Users import Users
from db_files.logger import Logger
from abc import ABC, abstractmethod
from tables.Flights import Flights
from tables.Airline_Companies import Airline_Companies
from tables.Countries import Countries
from errors.error_password_too_short import PasswordTooShort


class FacadeBase(ABC):
    @abstractmethod
    def __init__(self, repo):
        self.repo = repo
        self.logger = Logger.get_instance()

    def check_token(self, user_type, token):
        if user_type == Administrators:
            if token.role == 'Administrator':
                return True
        if user_type == Airline_Companies:
            if token.role == 'Airline_Companies':
                return True
        if user_type == Customers:
            if token.role == 'Customer':
                return True
        return False

    def get_all_flights(self):
        self.logger.logger.info('flights has been shown!')
        return self.repo.get_all(Flights)

    def get_flight_by_id(self, id):
        self.logger.logger.debug('Looking for a flight ...')
        if not isinstance(id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        elif self.repo.get_by_id(Flights, id) is None:
            self.logger.logger.error(f' id*{id}*, was not found!')
            raise FlightNotFound
        else:
            self.logger.logger.info('Flight shown!')
            return self.repo.get_by_id(Flights, id)

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        self.logger.logger.debug(f'Looking for flight by parameters...')
        if not isinstance(origin_country_id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        elif not isinstance(destination_country_id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        elif not isinstance(date, datetime):
            self.logger.logger.error('Input must be Input must be a datetime object!')
            raise Invalid_Input('Input must be a datetime object!')
        else:
            self.logger.logger.info('flights has been shown')
        return self.repo.get_by_condition(Flights, lambda query: query.filter(
            Flights.origin_country_id == origin_country_id,
            Flights.destination_country_id == destination_country_id,
            Flights.departure_time == date).all())

    def get_all_airlines(self):
        self.logger.logger.info('airlines has been shown!')
        return self.repo.get_all(Airline_Companies)

    def get_airline_by_id(self, id):
        self.logger.logger.debug(f'Looking for a airline *{id}*...')
        if not isinstance(id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        elif self.repo.get_by_id(Airline_Companies, id) is  None:
            self.logger.logger.error(f' id*{id}*, was not found!')
            raise AirlineNotFound
        else:
            self.logger.logger.info('airline  shown!')
            return self.repo.get_by_id(Airline_Companies, id)

    def get_airline_by_parameters(self, name, countries_id, country):
        self.logger.logger.debug(f'Looking for airline by parameters...')
        if not isinstance(name, Text):
            self.logger.logger.error('Input must be an text!')
            raise Invalid_Input('Input must be a text!')
        elif not isinstance(countries_id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        elif not isinstance(country, Text):
            self.logger.logger.error('Input must be an text!')
            raise Invalid_Input('Input must be a text!')
        else:
            self.logger.logger.info('airline has been shown')
        return self.repo.get_by_condition(Airline_Companies, lambda query: query.filter(
            Airline_Companies.name == name,
            Airline_Companies.countries_id == countries_id,
            Airline_Companies.country == country).all())

    def get_all_countries(self):
        self.logger.logger.info('Countries has been shown!')
        return self.repo.get_all(Countries)

    def get_country_by_id(self, id):
        self.logger.logger.debug(f'Looking for a country *{id}*...')
        if not isinstance(id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        elif self.repo.get_by_id(Countries, id) is None:
            self.logger.logger.error(f' id*{id}*, was not found!')
            raise InvalidCountry
        else:
            self.logger.logger.info('country  shown!')
            return self.repo.get_by_id(Countries, id)

    def create_new_user(self, user):
        if not isinstance(user, Users):
            self.logger.logger.error(' Input must be a "Users" object!')
            raise Invalid_Input('Input must be a "Users" object!')
        elif len(user.password) < 6:
            self.logger.logger.error(f'{PasswordTooShort} - Use at least 6 characters for the password!')
            raise PasswordTooShort
        self.logger.logger.info(f'User {user.username} created!')
        self.repo.add(user)

    def __str__(self):
        return f'{self.repo}'
