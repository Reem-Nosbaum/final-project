from errors.Invalid_Input import Invalid_Input
from facade.FacadeBase import FacadeBase
from db_files.logger import Logger
from LoginToken import LoginToken
from tables.Users import Users
from tables.Customers import Customers
from errors.error_Incorrect_password import IncorrectPassword
from errors.error_user_not_found import UserNotFound


class AnonymousFacade(FacadeBase):

    def __init__(self, repo):
        super().__init__(repo)
        self.logger = Logger.get_instance()
        self.login_token = LoginToken

    def login(self, username, password):
        self.logger.logger.debug('Attempting Logging-in...')
        if not isinstance(username, str):
            self.logger.logger.error('username must be string!')
            raise Invalid_Input
        elif not isinstance(password, str):
            self.logger.logger.error('password must be string!')
            raise Invalid_Input
        user = self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == username).all())
        if not user:
            self.logger.logger.error(f'The User-{username}- Not found')
            raise UserNotFound
        elif user[0].password != password:
            self.logger.logger.error('the password is incorrect')
            raise IncorrectPassword
        else:
            if user[0].user_role == 1:
                self.logger.logger.info(f'WELCOME, ADMIN {user[0].username}')
                return (LoginToken(id=user[0].administrators.user_id,
                                   name=user[0].administrators.first_name, role='Administrator'))
            elif user[0].user_role == 2:
                self.logger.logger.info(f'WELCOME, AIRLINE {user[0].username}')
                return (LoginToken(id=user[0].airline_companies.user_id,
                                   name=user[0].airline_companies.name, role='Airline_Companies'))
            elif user[0].user_role == 3:
                self.logger.logger.info(f'WELCOME, CUSTOMER {user[0].username}')
                return (LoginToken(id=user[0].customers.user_id,
                                   name=user[0].customers.first_name, role='Customer'))

    def add_customer(self, customer, user):
        self.logger.logger.debug('Setting up new customer and user...')
        if not isinstance(customer, Customers):
            self.logger.logger.error('Customer must be a "Customers" object!')
            raise Invalid_Input('Customer must be a "Customers" object!')
        else:
            self.create_new_user(user)
            self.logger.logger.info(f'User {user.username} created!')
            self.repo.add(customer)
            self.logger.logger.info(f'Customer {customer.first_name} {customer.last_name}  created!')
        super().create_new_user(user)

    def __str__(self):
        return f'<<Anonymous-Facade: {self.logger}>>'
