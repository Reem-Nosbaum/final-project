from datetime import datetime
from sqlalchemy import asc
from logger import Logger
from tables.Administrators import Administrators
from tables.Airline_Companies import Airline_Companies
from tables.Countries import Countries
from tables.Customers import Customers
from tables.Flights import Flights
from tables.Tickets import Tickets
from tables.User_Roles import User_Roles
from tables.Users import Users


class DbRepo:

    def __init__(self, local_session):
        self.local_session = local_session
        self.logger = Logger.get_instance()

    def reset_auto_inc(self, table_class):
        self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')
        self.logger.logger.debug(f'Reset auto inc in {table_class} table')

    def get_by_id(self, table_class, id):
        return self.local_session.query(table_class).get(id)

    def get_all(self, table_class):
        self.logger.logger.info('get all')
        return self.local_session.query(table_class).all()

    def get_all_limit(self, table_class, limit_num):
        return self.local_session.query(table_class).limit(limit_num).all()

    def get_all_order_by(self, table_class, column_name, direction=asc):
        return self.local_session.query(table_class).order_by(direction(column_name)).all()

    def get_by_condition(self, table_class, cond):
        query_result = self.local_session.query(table_class)
        result = cond(query_result)
        return result

    def get_by_column_value(self, table_class, column_name, value):
        return self.local_session.query(table_class).filter(column_name == value).all()

    def add(self, one_row):
        self.local_session.add(one_row)
        self.local_session.commit()
        self.logger.logger.debug(f'{one_row} has been added to the db')

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()
        self.logger.logger.debug(f'{rows_list} has been added to the db')

    def delete_table(self, table_name):
        self.local_session.execute(f'drop TABLE if exists {table_name} cascade')
        self.local_session.commit()
        self.logger.logger.debug(f'{table_name} has been deleted')

    def delete_by_id(self, table_class, id_column_name, id):
        self.local_session.query(table_class).filter(id_column_name == id).delete(synchronize_session=False)
        self.local_session.commit()
        self.logger.logger.debug(f'A row with the id {id} has been deleted from {table_class}')

    def update_by_id(self, table_class, id_column_name, id, data):
        self.local_session.query(table_class).filter(id_column_name == id).update(data)
        self.local_session.commit()
        self.logger.logger.debug(f'A row with the id {id} has been update from {table_class}')

    def update_by_column_value(self, table_class, column_name, value, data):
        self.local_session.query(table_class).filter(column_name == value).update(data)
        self.local_session.commit()
        print('updated')

    def get_by_ilike(self, table_class, column_name, exp):
        return self.local_session.query(table_class).filter(column_name.ilike(exp)).all()

# SP #
    def get_airline_by_username(self, _username):
        return self.local_session.execute(f'SELECT * FROM get_airline_by_username(\'{_username}\')')

    def get_customer_by_username(self, _username):
        return self.local_session.execute(f'SELECT * FROM get_customer_by_username(\'{_username}\')')

    def get_user_by_username(self, _username):
        return self.local_session.execute(f'SELECT * FROM get_user_by_username(\'{_username}\')')

    def get_flights_by_parameters(self, _origin_country_id, _destination_country_id, date):
        return self.local_session.execute(f'SELECT * FROM get_flights_by_parameters(\'{_origin_country_id}'
                                          f'{_destination_country_id}{date}\')')

    def get_flights_by_airline_id(self, _airline_id):
        return self.local_session.execute(f'SELECT * FROM get_flights_by_airline_id(\'{_airline_id}\')')

    def get_arrival_flights(self, _country_id):
        return self.local_session.execute(f'SELECT * FROM get_arrival_flights(\'{_country_id}\')')

    def get_departure_flights(self, _country_id):
        return self.local_session.execute(f'SELECT * FROM get_departure_flights(\'{_country_id}\')')

    def get_tickets_by_customer(self, _customer_id):
        return self.local_session.execute(f'SELECT * FROM get_departure_flights(\'{_customer_id}\')')

    def delete_all_tables(self):
        self.logger.logger.warning('deleting all tables.')
        self.delete_table('countries')
        self.delete_table('flights')
        self.delete_table('tickets')
        self.delete_table('airline_companies')
        self.delete_table('administrators')
        self.delete_table('customers')
        self.delete_table('users')
        self.delete_table('user_roles')

    def reset_all_tables_auto_inc(self):
        self.reset_auto_inc(Countries)
        self.reset_auto_inc(User_Roles)
        self.reset_auto_inc(Users)
        self.reset_auto_inc(Administrators)
        self.reset_auto_inc(Airline_Companies)
        self.reset_auto_inc(Customers)
        self.reset_auto_inc(Flights)
        self.reset_auto_inc(Tickets)

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
                      User_Roles(role_name='airline airline_company'),
                      User_Roles(role_name='customer')])

        self.add_all([Users(username='reem', password='reem123', email='reemn@jb.com', user_role=1),
                      Users(username='amit', password='amit98', email='amiti@jb.com', user_role=2),
                      Users(username='matan89', password='m12312', email='matan.m@jb.com', user_role=3),
                      Users(username='nir', password='niro23', email='niros@jb.com', user_role=3),
                      Users(username='or', password='lolo', email='orlo.m@jb.com', user_role=2),
                      Users(username='kim', password='kiril', email='kimi.m@jb.com', user_role=3)])

        self.add_all([Airline_Companies(name='Turkish airlines', countries_id=2, user_id=2),
                      Airline_Companies(name='Alaska airlines', countries_id=3, user_id=5)])

        self.add_all([Administrators(first_name='reem', last_name='nosbaum', user_id=1),
                      Administrators(first_name='amit', last_name='kuriel', user_id=2),
                      Administrators(first_name='matan', last_name='marom', user_id=3)])

        self.add_all([
            Customers(first_name='matan', last_name='marom', address='halolav 54',
                      phone_number='0508484582', credit_card_number='458003832839', user_id=3),
            Customers(first_name='or', last_name='cohen', address=' habrosh 85',
                      phone_number='0548736429', credit_card_number='532685938764', user_id=6)])

        self.add_all([Flights(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                              departure_time=datetime(2022, 1, 1, 10, 10, 10),
                              landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=0),
                      Flights(airline_company_id=2, origin_country_id=2,
                              destination_country_id=1, departure_time=datetime(2022, 3, 18, 10, 12, 10),
                              landing_time=datetime(2022, 12, 4, 23, 29, 1), remaining_tickets=3),
                      Flights(airline_company_id=2, origin_country_id=3, destination_country_id=2,
                              departure_time=datetime(2022, 1, 2, 10, 12, 10),
                              landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=400),
                      Flights(airline_company_id=1, origin_country_id=1, destination_country_id=3,
                              departure_time=datetime(2022, 1, 2, 10, 12, 10),
                              landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=0)])

        self.add_all([Tickets(flight_id=1, customer_id=1),
                      Tickets(flight_id=1, customer_id=2),
                      Tickets(flight_id=3, customer_id=2)])
