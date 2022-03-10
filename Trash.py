# deletion of existing input
repo.delete_table('countries')
repo.delete_table('flights')
repo.delete_table('tickets')
repo.delete_table('airline_companies')
repo.delete_table('administrators')
repo.delete_table('customers')
repo.delete_table('users')
repo.delete_table('user_roles')

create_all_entities()




repo.add_all(countries_list := [Countries(name='israel'), Countries(name='italy')])

repo.add_all(user_roles_list := [User_Roles(role_name='administrator'),
                                 User_Roles(role_name='airline company'),
                                 User_Roles(role_name='customer')])

repo.add_all(users_list := [Users(username='ron32', password='ron123', email='ron95@jb.com', user_role=1),
                            Users(username='reem26', password='reem96', email='reemnu@jb.com', user_role=2),
                            Users(username='or.co', password='or123', email='or.cohen95@jb.com', user_role=3),
                            Users(username='boris45', password='boris3', email='boris.m@jb.com', user_role=1),
                            Users(username='lola', password='lola_e', email='lole5@jb.com', user_role=2),
                            Users(username='orlev', password='or123', email='or@jb.com', user_role=3)])

repo.add_all(airline_companies_list := [Airline_Companies(name='el-al', countries_id=1, user_id=1),
                                        Airline_Companies(name='turkish airlines', countries_id=2, user_id=2)])

repo.add_all(administrators_list := [Administrators(first_name='reem', last_name='nosbaum', user_id=1),
                                     Administrators(first_name='amit', last_name='kuriel', user_id=2)],
                                     Administrators(first_name='reem', last_name='nosbaum', user_id=3),
                                     Administrators(first_name='amit', last_name='kuriel', user_id=4)
                                    Administrators(first_name='reem', last_name='nosbaum', user_id=5)])

repo.add_all(customers_list := [Customers(first_name='ron', last_name='ben david', address='hertzel 54',
                                          phone_number='0508493382', credit_card_number='458095432839', user_id=1),
                                Customers(first_name='reem', last_name='yaniv', address='bit el 85',
                                          phone_number='0548938829', credit_card_number='532685932833', user_id=2),
                                Customers(first_name='or', last_name='lokA', address='halolav 54',
                                          phone_number='0508484582', credit_card_number='458003832839', user_id=3),
                                Customers(first_name='boris', last_name='musnikov', address=' habrosh 85',
                                          phone_number='0548736429', credit_card_number='532685938764', user_id=4),
                                Customers(first_name='lola', last_name='boka', address='roshan 54',
                                          phone_number='0504563582',
                                          credit_card_number='458003958339', user_id=5),
                                Customers(first_name='orlev', last_name='cohen', address=' shokolad 55',
                                          phone_number='0508332273',
                                          credit_card_number='532698438764', user_id=6)])

repo.add_all(flights_list := [Flights(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                      departure_time=datetime.now(), landing_time=datetime(2022, 10, 4, 14, 29, 1),
                                      remaining_tickets=0), Flights(airline_company_id=2, origin_country_id=2,
                                                                    destination_country_id=1,
                                                                    departure_time=datetime.now(),
                                                                    landing_time=datetime(2022, 12, 4, 23, 29, 1),
                                                                    remaining_tickets=0)])

repo.add_all(tickets_list := [Tickets(flight_id=1, customer_id=1),
                              Tickets(flight_id=2, customer_id=2)])


#        if flight.remaining_tickets < 1:
#            raise NoMoreTicketsForFlights


##        user = self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == username).all())
       # if not user:
        #    self.logger.logger.error(f'The User-{username}- Not found')
       #     raise error_user_not_found
      #  if user[0].password != password:
       #     self.logger.looger.error('the password is incorrect')
      #  elif user.user_role[0] == 1:
     #       self.logger.looger.info(f'WELCOM, ADMIN {user[0].username}')
    #    elif user.user_role[0] == 2:
   #         self.logger.looger.info(f'WELCOM, AIRLINE {user[0].username}')
  #      elif user.user_role[0] == 3:
 #           self.logger.looger.info(f'WELCOME, CUSTOMER {user[0].username}')
#        else:
##





from errors import error_user_not_found
from errors.Invalid_Input import Invalid_Input
from facade.Administrator_Facade import AdministratorFacade
from facade.Customer_Facade import CustomerFacade
from facade.FacadeBase import FacadeBase
from logger import Logger
from errors.error_password_too_short import PasswordTooShort
from LoginToken import LoginToken
from tabels.Users import Users
from tabels.Customers import Customers
from errors.error_Incorrect_password import IncorrectPassword
from errors.error_user_not_found import UserNotFound


class AnonymousFacade(FacadeBase):

    def __init__(self, repo):
        super().__init__(repo)
        self.logger = Logger.get_instance()
        self.login_token = LoginToken

    ########  need to check this fun ######
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
            self.logger.looger.error('the password is incorrect')
            raise IncorrectPassword
        else:
            if user[0].user_role == 1:
                self.logger.looger.info(f'WELCOME, ADMIN {user[0].username}')
                return (LoginToken(id=user[0].administrators.user_id,
                                   name=user[0].administrators.first_name, role='Administrator'))
            elif user[0].user_role == 2:
                self.logger.looger.info(f'WELCOME, AIRLINE {user[0].username}')
                return (LoginToken(id=user[0].airline_companies.user_id,
                                   name=user[0].airline_companies.name, role='Airline'))
            elif user[0].user_role == 3:
                self.logger.looger.info(f'WELCOME, CUSTOMER {user[0].username}')
                return (LoginToken(id=user[0].customers.user_id,
                                   name=user[0].customers.first_name, role='Customer'))



    def add_customer(self, customer, user):
        self.logger.logger.debug('Setting up new customer and user...')
        if not isinstance(customer, Customers):
            self.logger.logger.error('Admin must be a "Customers" object!')
        elif len(user.password) < 6:
            self.logger.logger.error(f'{PasswordTooShort} - Use at least 6 characters for the password!')
        elif user.user_role == 3:
            self.create_new_user(customer)
            self.logger.logger.info(f'User {user.username} created!')
            self.repo.add(customer)
            self.logger.logger.info(f'Customer {customer.first_name} {customer.last_name}  created!')
        super().create_new_user(user)




        elif self.repo.get_by_id(Users, administrator.user_id) is not None:


        elif self.repo.get_user_by_username(user.username) is not None:




    def reset_db(self):
        self.logger.logger.debug(f'resetting initial DB.')
        self.reset_auto_inc(Countries)
        self.reset_auto_inc(Users)
        self.reset_auto_inc(Airline_Companies)
        self.reset_auto_inc(Customers)
        self.reset_auto_inc(Flights)
        self.reset_auto_inc(Tickets)
        self.reset_auto_inc(Administrators)
        self.reset_auto_inc(User_Roles)

        self.add_all([Countries(name='Israel'),
                      Countries(name='China'),
                      Countries(name='Cuba'),
                      Countries(name='France'),
                      Countries(name='Mexico'),
                      Countries(name='italy'),
                      Countries(name='Russia'),
                      Countries(name='Zimbabwe')])

        self.add_all([User_Roles(role_name='administrator'),
                      User_Roles(role_name='airline company'),
                      User_Roles(role_name='customer')])

        self.add_all([Users(username='reem', password='reem123', email='reemn@jb.com', user_role=1),
                      Users(username='amit', password='amit98', email='amiti@jb.com', user_role=2),
                      Users(username='or', password='oror2', email='or.cohen95@jb.com', user_role=3),
                      Users(username='boris', password='boris3', email='boris.m@jb.com', user_role=1),
                      Users(username='matan', password='m12312', email='matan.m@jb.com', user_role=2),
                      Users(username='nir', password='niro23', email='niros@jb.com', user_role=3),
                      Users(username='test', password='test123', email='test.m@jb.com', user_role=1),
                      Users(username='test2', password='test123', email='test2.m@jb.com', user_role=2),
                      Users(username='test3', password='test1234', email='test3.m@jb.com', user_role=3)])

        self.add_all([Airline_Companies(name='el al', countries_id=1, user_id=1),
                      Airline_Companies(name='Turkish airlines', countries_id=2, user_id=2),
                      Airline_Companies(name='Alaska airlines', countries_id=3, user_id=3),
                      Airline_Companies(name='American airlines', countries_id=4, user_id=4),
                      Airline_Companies(name='Breeze airways', countries_id=3, user_id=5),
                      Airline_Companies(name='test air', countries_id=6, user_id=8),
                      Airline_Companies(name='Hawaiian airlines', countries_id=4, user_id=6)])

        self.add_all([Administrators(first_name='reem', last_name='nosbaum', user_id=1),
                      Administrators(first_name='amit', last_name='kuriel', user_id=2),
                      Administrators(first_name='or', last_name='cohen', user_id=3),
                      Administrators(first_name='boris', last_name='mosnikov', user_id=4),
                      Administrators(first_name='matan', last_name='marom', user_id=5),
                      Administrators(first_name='nir', last_name='levi', user_id=6),
                      Administrators(first_name='teste', last_name='testo', user_id=7)])

        self.add_all([
            Customers(first_name='reem', last_name='nosbaum', address='hertzel 54',
                      phone_number='0508493382', credit_card_number='458095432839', user_id=1),
            Customers(first_name='amit', last_name='kuriel', address='bit el 85',
                      phone_number='0548938829', credit_card_number='532685932833', user_id=2),
            Customers(first_name='or', last_name='cohen', address='halolav 54',
                      phone_number='0508484582', credit_card_number='458003832839', user_id=3),
            Customers(first_name='boris', last_name='musnikov', address=' habrosh 85',
                      phone_number='0548736429', credit_card_number='532685938764', user_id=4),
            Customers(first_name='matan', last_name='marom', address='roshan 54',
                      phone_number='0504563582', credit_card_number='458003958339', user_id=5),
            Customers(first_name='nir', last_name='levi', address=' shokolad 55',
                      phone_number='0508332273', credit_card_number='532698438764', user_id=6),
            Customers(first_name='test', last_name='test3', address='rere 54',
                      phone_number='05045543582', credit_card_number='458004448339', user_id=9)])

        self.add_all([
            Flights(airline_company_id=1, origin_country_id=1,
                    destination_country_id=2, departure_time=datetime(2022, 10, 4, 10, 29, 1),
                    landing_time=datetime(2022, 10, 4, 14, 29, 1), remaining_tickets=6),
            Flights(airline_company_id=2, origin_country_id=2,
                    destination_country_id=1, departure_time=datetime(2022, 12, 4, 21, 29, 1),
                    landing_time=datetime(2022, 12, 4, 23, 29, 1), remaining_tickets=0),
            Flights(airline_company_id=3, origin_country_id=3, destination_country_id=1,
                    departure_time=datetime(2022, 11, 5, 8, 00, 1),
                    landing_time=datetime(2022, 11, 5, 10, 34, 10),
                    remaining_tickets=0)])

        self.add_all([Tickets(flight_id=1, customer_id=1),
                      Tickets(flight_id=2, customer_id=3)])
