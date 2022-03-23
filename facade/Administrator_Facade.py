from errors.Invalid_Input import Invalid_Input
from errors.Invalid_Toke import InvalidToken
from errors.error_user_exist import UserAlreadyExist
from facade.FacadeBase import FacadeBase
from tabels.Customers import Customers
from tabels.Airline_Companies import Airline_Companies
from tabels.Administrators import Administrators
from logger import Logger
from errors.error_password_too_short import PasswordTooShort
from LoginToken import LoginToken
from tabels.Users import Users


class AdministratorFacade(FacadeBase):

    def __init__(self, repo):
        super().__init__(repo)
        self.logger = Logger.get_instance()
        self.login_token = LoginToken

    def get_all_customers(self, token):
        if not self.check_token(Administrators, token):
            raise InvalidToken
        self.logger.logger.info('customers has been shown!...')
        return self.repo.get_all(Customers)

    def add_airline(self, airline, user, token):
        if not self.check_token(Administrators, token):
            self.logger.logger.debug('creating a new airline and user...')
            raise InvalidToken
        if not isinstance(airline, Airline_Companies):
            self.logger.logger.error('Admin must be a "Airline_Companies" object!')
            raise Invalid_Input('Input must be a "AirlineCompanies" object!')
        if not isinstance(user, Users):
            self.logger.logger.error(f'{Invalid_Input} - User must be a "Users" object!')
            raise Invalid_Input('Input must be a "Users" object!')
        elif self.repo.get_by_id(Users, user.id) is not None: # get user by username - (user.username)
            self.logger.logger.error(f'{UserAlreadyExist} - User-ID {airline.user_id} already in use!')
            raise UserAlreadyExist
        elif user.user_role == 2:
            self.create_new_user(user)
            self.logger.logger.info(f'User {user.username} created!')
            self.repo.add(airline)
            self.logger.logger.info(f'airline created!')

    def add_customer(self, customer, user, token):
        if not self.check_token(Administrators, token):
            self.logger.logger.debug('creating a new customer and user...')
            raise InvalidToken
        if not isinstance(customer, Customers):
            self.logger.logger.error('Admin must be a "Customers" object!')
            raise Invalid_Input('Admin must be a "Customers" object!')
        if not isinstance(user, Users):
            self.logger.logger.error(f'{Invalid_Input} - User must be a "Users" object!')
            raise Invalid_Input('Input must be a "Users" object!')
        elif len(user.password) < 6:
            self.logger.logger.error(f'{PasswordTooShort} - Use at least 6 characters for the password!')
            raise PasswordTooShort('Use at least 6 characters for the password!')
        elif self.repo.get_by_id(Users, user.id) is not None:
            self.logger.logger.error(f'{UserAlreadyExist} - User-ID {customer.user_id} already in use!')
            raise UserAlreadyExist
        elif user.user_role == 3:
            self.create_new_user(user)
            self.logger.logger.info(f'User {user.username} created!')
            self.repo.add(customer)
            self.logger.logger.info(f'Customer {customer.first_name} {customer.last_name}  created!')

    def add_administrator(self, administrator, user, token):
        if not self.check_token(Administrators, token):
            self.logger.logger.debug('creating a new customer and user...')
            raise InvalidToken
        if not isinstance(administrator, Administrators):
            self.logger.logger.error('Admin must be a "Administrators" object!')
            raise Invalid_Input('Input must be a "Administrators" object!')
        if not isinstance(user, Users):
            self.logger.logger.error(f'{Invalid_Input} - User must be a "Users" object!')
            raise Invalid_Input('Input must be a "Users" object!')
        elif self.repo.get_by_id(Users, user.id) is not None:
            self.logger.logger.error(f'{UserAlreadyExist} - User-ID {administrator.user_id} already in use!')
            raise UserAlreadyExist
        elif user.user_role == 1:
            self.create_new_user(user)
            self.logger.logger.info(f'User {user.username} created!')
            self.repo.add(administrator)
            self.logger.logger.info(f'adnim {administrator.first_name} {administrator.last_name}  created!')

    def remove_airline(self, airline_id, token):
        if not self.check_token(Administrators, token):
            self.logger.logger.debug('removing airline ...')
            raise InvalidToken
        airline1 = self.repo.get_by_id(Airline_Companies, airline_id)
        if not isinstance(airline_id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        else:
            self.repo.delete_by_id(Airline_Companies, Airline_Companies.id, airline_id)
            self.logger.logger.info(f'Airline #{airline_id} Deleted!')
            self.repo.delete_by_id(Users, Users.id, airline1)
            self.logger.logger.info(f'User #{airline_id} Deleted!')

    def remove_customer(self, customer_id, token):
        if not self.check_token(Administrators, token):
            self.logger.logger.debug('removing customer ...')
            raise InvalidToken
        customer1 = self.repo.get_by_id(Customers, customer_id)
        if not isinstance(customer_id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        else:
            self.repo.delete_by_id(Customers, Customers.id, customer_id)
            self.logger.logger.info('customer Deleted!')
            self.repo.delete_by_id(Users, Users.id, customer1)
            self.logger.logger.info(f'User #{customer_id} Deleted!')

    def remove_administrator(self, administrator_id, token):
        if not self.check_token(Administrators, token):
            self.logger.logger.debug('removing administrator ...')
            raise InvalidToken
        admin1 = self.repo.get_by_id(Administrators, administrator_id)
        if not isinstance(administrator_id, int):
            self.logger.logger.error('Input must be an integer!')
            raise Invalid_Input('Input must be an integer!')
        else:
            self.repo.delete_by_id(Administrators, Administrators.id, administrator_id)
            self.logger.logger.info('administrator Deleted!')
            self.repo.delete_by_id(Users, Users.id, admin1.user_id)
            self.logger.logger.info(f'User Deleted!')

    def __str__(self):
        return f'{super().__init__}'
