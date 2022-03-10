import pytest
from LoginToken import LoginToken
from errors.Invalid_Input import Invalid_Input
from errors.error_password_too_short import PasswordTooShort
from errors.error_user_exist import UserAlreadyExist
from facade.Anonymous_Facade import AnonymousFacade
from facade.Administrator_Facade import AdministratorFacade
from db_config import local_session, config
from db_repo import DbRepo
from tabels.Administrators import Administrators
from tabels.Airline_Companies import Airline_Companies
from tabels.Customers import Customers
from tabels.Users import Users

repo = DbRepo(local_session)


@pytest.fixture(scope='session')
def admin_facade_object():
    return AdministratorFacade(repo)


@pytest.fixture(scope='session')
def admin_token():
    an_facade = AnonymousFacade(repo)
    return an_facade.login('reem', 'reem123')


@pytest.fixture(scope='function', autouse=True)
def admin_facade_clean():
    repo.reset_db()


def test_get_all_customers(admin_facade_object, admin_token):
    assert admin_facade_object.get_all_customers(admin_token) == repo.get_all(Customers)


def test_add_administrator(admin_facade_object, admin_token):
    expected_admin = Administrators(first_name='testomry', last_name='testnosbaum', user_id=7)
    expected_user = Users(username='testor', password='testcohen', email='orc@jb.com', user_role=1)
    admin_facade_object.add_administrator(expected_admin, expected_user, admin_token)
    check_admin = repo.get_by_id(Administrators, 7)
    check_user = repo.get_by_id(Users, 7)
    assert check_admin == expected_admin
    assert check_user == expected_user


#bug
def test_not_add_administrator(admin_facade_object, admin_token):
    with pytest.raises(Invalid_Input):
        expected_admin = Administrators(first_name='testomry', last_name='testnosbaum', user_id=3)
        expected_user = "Users(username='testomri', password='testomre', email='testomre@jb.com', user_role=1)"
        admin_facade_object.add_administrator(expected_admin, expected_user, admin_token)
    with pytest.raises(Invalid_Input):
        expected_admin = "Administrators(first_name='testomry', last_name='testnosbaum', user_id=3)"
        expected_user = Users(username='testomri', password='testomre', email='testomre@jb.com', user_role=1)
        admin_facade_object.add_administrator(expected_admin, expected_user, admin_token)
    with pytest.raises(UserAlreadyExist):
        expected_admin = Administrators(first_name='testomry', last_name='testnosbaum', user_id=7)
        expected_user = Users(username='testomri', password='testomre', email='testomre@jb.com', user_role=1)
        admin_facade_object.add_administrator(expected_admin, expected_user, admin_token)
    with pytest.raises(PasswordTooShort):
        expected_admin = Administrators(first_name='testomry', last_name='testnosbaum', user_id=7)
        expected_user = Users(username='testor', password='12', email='orc@jb.com', user_role=1)
        admin_facade_object.add_administrator(expected_admin, expected_user, admin_token)


def test_add_airline(admin_facade_object, admin_token):
    expected_airline = Airline_Companies(name='bodako air', countries_id=7, user_id=7)
    expected_user = Users(username='testomri', password='testomre', email='testomre@jb.com', user_role=1)
    admin_facade_object.add_airline(expected_airline, expected_user, admin_token)
    check_airline = repo.get_by_id(Airline_Companies, 7)
    check_user = repo.get_by_id(Users, 7)
    assert check_airline == expected_airline
    assert check_user == expected_user


#BUG
def test_not_add_airline(admin_facade_object, admin_token):
    with pytest.raises(Invalid_Input):
        expected_airline = "Airline_Companies(name='bodako air', countries_id=7, user_id=7)"
        expected_user = Users(username='testshir', password='shir1234', email='shir23@jb.com', user_role=1)
        admin_facade_object.add_airline(expected_airline, expected_user, admin_token)
    with pytest.raises(Invalid_Input):
        expected_airline = "AirlineCompanies(name='bodako air', countries_id=7, user_id=7)"
        expected_user = Users(username='testshir', password='shir1234', email='shir23@jb.com', user_role=1)
        admin_facade_object.add_airline(expected_airline, expected_user, admin_token)
    with pytest.raises(UserAlreadyExist):
        expected_airline = Airline_Companies(name='bodako air', countries_id=7, user_id=7)
        expected_user = Users(username='testshir', password='shir1234', email='shir23@jb.com', user_role=1)
        admin_facade_object.add_airline(expected_airline, expected_user, admin_token)
    with pytest.raises(PasswordTooShort):
        expected_airline = Airline_Companies(name='bodako air', countries_id=7, user_id=7)
        expected_user = Users(username='testomri', password='12', email='testomre@jb.com', user_role=1)
        admin_facade_object.add_airline(expected_airline, expected_user, admin_token)


def test_add_customer(admin_facade_object, admin_token):
    expected_customer = Customers(first_name='testkobi', last_name='testnaroto', address='gosher 31',
                                  phone_number='test0584739928', credit_card_number='test45809843', user_id=7)
    expected_user = Users(username='testor', password='testcohen', email='orc@jb.com', user_role=1)
    admin_facade_object.add_customer(expected_customer, expected_user, admin_token)
    check_customer = repo.get_by_id(Customers, 7)
    check_user = repo.get_by_id(Users, 7)
    assert check_customer == expected_customer
    assert check_user == expected_user


def test_not_add_customer(admin_facade_object, admin_token):
    with pytest.raises(Invalid_Input):
        expected_customer = "Customers(first_name='testkobi', last_name='testnaroto', address='gosher 31'," \
                            " phone_number='test0584739928', credit_card_number='test45809843', user_id=7)"
        expected_user = Users(username='testkob', password='testko', email='kobi95@jb.com', user_role=1)
        admin_facade_object.add_customer(expected_customer, expected_user, admin_token)
    with pytest.raises(Invalid_Input):
        expected_customer = Customers(first_name='testkobi', last_name='testnaroto', address='gosher 31',
                                      phone_number='test0584739928', credit_card_number='test45809843', user_id=7)
        expected_user = "Users(username='testkob', password='testkoko', email='kobi95@jb.com', user_role=1)"
        admin_facade_object.add_customer(expected_customer, expected_user, admin_token)
    with pytest.raises(UserAlreadyExist):
        expected_customer = Customers(first_name='testkobi', last_name='testnaroto', address='gosher 31',
                                      phone_number='test0584739928', credit_card_number='test45809843', user_id=7)
        expected_user = Users(username='testkob', password='testkoko', email='kobi95@jb.com', user_role=1)
        admin_facade_object.add_customer(expected_customer, expected_user, admin_token)
    with pytest.raises(PasswordTooShort):
        expected_customer = Customers(first_name='testkobi', last_name='testnaroto', address='gosher 31',
                                      phone_number='test0584739928', credit_card_number='test45809843', user_id=7)
        expected_user = Users(username='testkob', password='12', email='kobi95@jb.com', user_role=1)
        admin_facade_object.add_customer(expected_customer, expected_user, admin_token)


def test_remove_administrator(admin_facade_object, admin_token):
    admin_facade_object.remove_administrator(1, admin_token)
    assert repo.get_by_id(Administrators, 1) is None
    assert repo.get_by_id(Users, 1) is None


def test_not_remove_administrator(admin_facade_object, admin_token):
    with pytest.raises(Invalid_Input):
        admin_facade_object.remove_administrator('3', admin_token)

#bug
def test_remove_airline(admin_facade_object, admin_token):
    admin_facade_object.remove_airline(2, admin_token)
    assert repo.get_by_id(Airline_Companies, 2) is None
    assert repo.get_by_id(Users, 5) is None


def test_not_remove_airline(admin_facade_object, admin_token):
    with pytest.raises(Invalid_Input):
        admin_facade_object.remove_airline('3', admin_token)


def test_remove_customer(admin_facade_object, admin_token):
    admin_facade_object.remove_customer(2, admin_token)
    assert repo.get_by_id(Customers, 2) is None
    assert repo.get_by_id(Users, 6) is None


def test_not_remove_customer(admin_facade_object, admin_token):
    with pytest.raises(Invalid_Input):
        admin_facade_object.remove_customer('4', admin_token)
