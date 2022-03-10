from datetime import datetime

import pytest

from LoginToken import LoginToken
from Tests.test_admin_facade import admin_token
from db_config import local_session
from db_repo import DbRepo
from errors.Invalid_Input import Invalid_Input
from errors.Invalid_Toke import InvalidToken
from errors.error_airline_not_found import AirlineNotFound
from errors.error_flight_not_found import FlightNotFound
from facade.Airline_Facade import AirlineFacade
from facade.Anonymous_Facade import AnonymousFacade
from tabels.Airline_Companies import Airline_Companies
from tabels.Flights import Flights

repo = DbRepo(local_session)


@pytest.fixture(scope='session')
def airline_facade_object():
    return AirlineFacade(repo)


@pytest.fixture(scope='session')
def airline_token():
    an_facade = AnonymousFacade(repo)
    return an_facade.login('matan', 'm123')


@pytest.fixture(scope='function', autouse=True)
def airline_facade_clean():
    repo.reset_db()


def test_get_flights_by_airline(airline_facade_object, airline_token):
    assert airline_facade_object.get_flights_by_airline(3, airline_token) ==\
           repo.get_by_column_value(Flights, Flights.airline_company_id, 3)


def test_not_get_flights_by_airline(airline_facade_object, airline_token):
    with pytest.raises(Invalid_Input):
        airline_facade_object.get_flights_by_airline('t', airline_token)
    with pytest.raises(AirlineNotFound):
        airline_facade_object.get_flights_by_airline(11, airline_token)
        invalid_token = LoginToken(0, 'BS', 10)
        airline_facade_object.get_flights_by_airline(1, invalid_token)


def test_add_flight(airline_facade_object, airline_token):
    expected_flight = Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2,
                              departure_time=datetime(2022, 1, 4, 10, 10, 10),
                              landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)
    airline_facade_object.add_flight(expected_flight, airline_token)
    check_flight = repo.get_by_id(Flights, 4)
    assert check_flight == expected_flight


def test_not_add_flight(airline_facade_object, airline_token):
    with pytest.raises(Invalid_Input):
        flight = 'Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2,' \
                 ' departure_time=datetime(2023, 1, 4, 10, 10, 10),' \
                 ' landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)'
        airline_facade_object.add_flight(flight, airline_token)
        invalid_token = LoginToken(0, 'BS', 10)
        flight = Flights(airline_company_id=1, origin_country_id=3, destination_country_id=2,
                         departure_time=datetime(2022, 1, 4, 10, 10, 10),
                         landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)
        airline_facade_object.add_flight(flight, invalid_token)


def test_update_airline(airline_facade_object, airline_token):
    airline_update = {'name': 'Up Yours LTD'}
    airline_facade_object.update_airline(airline_update, 2, airline_token)
    check_airline = repo.get_by_id(Airline_Companies, 2)
    assert check_airline.name == 'Up Yours LTD'


def test_not_update_airline(airline_facade_object, airline_token):
    with pytest.raises(Invalid_Input):
        airline_update = "{'name':'Up Yours LTD'}"
        airline_facade_object.update_airline(airline_update, 2, airline_token)
    with pytest.raises(Invalid_Input):
        airline_update = {'name': 'Up Yours LTD'}
        airline_facade_object.update_airline(airline_update, 't', airline_token)
        invalid_token = LoginToken(0, 'BS', 10)
        airline_update = {'name': 'Up Yours LTD'}
        airline_facade_object.update_airline(airline_update, 1, invalid_token)


def test_update_flight(airline_facade_object, airline_token):
    flight_update = {'departure_time': datetime(2022, 1, 1, 11, 10, 10), 'remaining_tickets': 12332}
    airline_facade_object.update_flight(flight_update, 2, airline_token)
    check_flight = repo.get_by_id(Flights, 2)
    assert check_flight.departure_time == datetime(2022, 1, 1, 11, 10, 10)
    assert check_flight.remaining_tickets == 12332


def test_not_update_flight(airline_facade_object, airline_token):
    with pytest.raises(Invalid_Input):
        airline_facade_object.update_flight("{'remaining_tickets': -2}", 2, airline_token)
    with pytest.raises(Invalid_Input):
        airline_facade_object.update_flight({'remaining_tickets': 2}, 'ty', airline_token)
    with pytest.raises(FlightNotFound):
        airline_facade_object.update_flight({'remaining_tickets': 2}, 52, airline_token)
        invalid_token = LoginToken(0, 'BS', 10)
        airline_facade_object.update_flight({'remaining_tickets': 2}, 1, invalid_token)


def test_remove_flight(airline_facade_object, airline_token):
    airline_facade_object.remove_flight(3, airline_token)
    assert repo.get_by_id(Flights, 3) is None


def test_not_remove_flight(airline_facade_object, airline_token):
    with pytest.raises(Invalid_Input):
        airline_facade_object.remove_flight('tr', airline_token)
    with pytest.raises(FlightNotFound):
        airline_facade_object.remove_flight(78, airline_token)
    invalid_token = LoginToken(0, 'BS', 10)
    with pytest.raises(InvalidToken):
        airline_facade_object.remove_flight(1, invalid_token)

