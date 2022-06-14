from datetime import datetime
import pytest
from db_config import local_session
from db_files.db_repo import DbRepo
from errors.error_airline_not_found import AirlineNotFound
from errors.error_invalid_country import InvalidCountry
from errors.error_password_too_short import PasswordTooShort
from tables.Airline_Companies import Airline_Companies
from tables.Countries import Countries
from tables.Flights import Flights
from facade.Anonymous_Facade import AnonymousFacade
from errors.Invalid_Input import Invalid_Input
from errors.error_flight_not_found import FlightNotFound
from tables.Users import Users

repo = DbRepo(local_session)
anonymous_facade = AnonymousFacade(repo)


@pytest.fixture(scope='session')
def base_facade_object():
    an_facade = anonymous_facade
    return an_facade


@pytest.fixture(scope='function', autouse=True)
def anonymous_facade_clean():
    repo.reset_db()


def test_get_all_flights(base_facade_object):
    assert base_facade_object.get_all_flights() == repo.get_all(Flights)


def test_get_flight_by_id(base_facade_object):
    assert base_facade_object.get_flight_by_id(1) == repo.get_by_id(Flights, 1)


def test_not_get_flight_by_id(base_facade_object):
    with pytest.raises(Invalid_Input):
        base_facade_object.get_flight_by_id('1')
    with pytest.raises(FlightNotFound):
        base_facade_object.get_flight_by_id(345)


def test_get_flights_by_parameters(base_facade_object):
    actual_flight = base_facade_object.get_flights_by_parameters(1, 2, datetime(2022, 1, 1, 10, 10, 10))[0]

    expected_flight = Flights()
    expected_flight.id = 1
    expected_flight.airline_company_id = 1
    expected_flight.origin_country_id = 1
    expected_flight.destination_country_id = 2
    expected_flight.departure_time = datetime(2022, 1, 1, 10, 10, 10)
    expected_flight.landing_time = datetime(2022, 1, 24, 10, 29, 1)
    expected_flight.remaining_tickets = 0

    assert actual_flight.id == expected_flight.id
    assert actual_flight.airline_company_id == 1
    assert actual_flight.origin_country_id == 1


def test_not_get_flights_by_parameters(base_facade_object):
    with pytest.raises(Invalid_Input):
        base_facade_object.get_flights_by_parameters('1', 2, datetime(2022, 1, 1, 10, 10, 10))
    with pytest.raises(Invalid_Input):
        base_facade_object.get_flights_by_parameters(1, '2', datetime(2022, 1, 1, 10, 10, 10))
    with pytest.raises(Invalid_Input):
        base_facade_object.get_flights_by_parameters(1, 2, 'datetime(2022, 1, 1, 10, 10, 10)')


def test_get_all_airlines(base_facade_object):
    assert base_facade_object.get_all_airlines() == repo. get_all(Airline_Companies)


def test_get_airline_by_id(base_facade_object):
    assert base_facade_object.get_airline_by_id(1) == repo.get_by_id(Airline_Companies, 1)


def test_not_get_airline_by_id(base_facade_object):
    with pytest.raises(Invalid_Input):
        base_facade_object.get_airline_by_id('1')
    with pytest.raises(AirlineNotFound):
        base_facade_object.get_airline_by_id(563)


def test_get_all_countries(base_facade_object):
    assert base_facade_object.get_all_countries() == repo. get_all(Countries)


def test_get_country_by_id(base_facade_object):
    assert base_facade_object.get_country_by_id(1) == repo.get_by_id(Countries, 1)


def test_not_get_country_by_id(base_facade_object):
    with pytest.raises(Invalid_Input):
        base_facade_object.get_country_by_id('1')
    with pytest.raises(InvalidCountry):
        base_facade_object.get_country_by_id(894)


def test_create_user(base_facade_object):
    base_facade_object.create_new_user(Users(username='testReem', password='1234567', email='testreem@jb.com',
                                             user_role=3))
    assert repo.get_by_column_value(Users, Users.username, 'testReem') is not None


def test_not_create_user(base_facade_object):
    with pytest.raises(Invalid_Input):
        base_facade_object.create_new_user('3')
    with pytest.raises(PasswordTooShort):
        base_facade_object.create_new_user(Users(username='testReem', password='123', email='testreem@jb.com',
                                                 user_role=3))
