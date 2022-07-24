import pytest
from db_config import local_session
from db_repo import DbRepo
from errors.Invalid_Input import Invalid_Input
from errors.error_Incorrect_password import IncorrectPassword
from errors.error_user_not_found import UserNotFound
from facade.Anonymous_Facade import AnonymousFacade
from tables.Customers import Customers
from tables.Users import Users

repo = DbRepo(local_session)
anonymous_facade = AnonymousFacade(repo)


@pytest.fixture(scope='session')
def anonymous_facade_object():
    an_facade = anonymous_facade
    return an_facade


@pytest.fixture(scope='function', autouse=True)
def anonymous_facade_clean():
    repo.reset_db()


def test_login(anonymous_facade_object):
    assert anonymous_facade_object.login('reem', 'reem123') is not None


def test_not_login(anonymous_facade_object):
    with pytest.raises(Invalid_Input):
        anonymous_facade_object.login('reem', 1234)
    with pytest.raises(Invalid_Input):
        anonymous_facade_object.login(1234, 'reem123')
    with pytest.raises(UserNotFound):
        anonymous_facade_object.login('sean12', 'reem95')
    with pytest.raises(IncorrectPassword):
        anonymous_facade_object.login('reem', 'reem124')


def test_add_customer(anonymous_facade_object):
    expected_customer = Customers(first_name='test', last_name='one', address='nhalal 54',
                                  phone_number='test0504933826', credit_card_number='test4580543728394', user_id=7)
    expected_user = Users(username='test', password='test123', email='testorl@jb.com', user_role=3)
    anonymous_facade_object.add_customer(expected_customer, expected_user)
    assert repo.get_by_column_value(Customers, Customers.first_name, 'test') is not None
    assert repo.get_by_column_value(Users, Users.username, 'test') is not None


def test_not_add_customer(anonymous_facade_object):
    with pytest.raises(Invalid_Input):
        expected_customer = "Customers(first_name='test', last_name='testo', address='hgosrim 45'," \
                            " phone_number='test0528795548', credit_card_number='test38748593', user_id=3)"
        expected_user = Users(username='test2', password='test321', email='test34a@jb.com', user_role=3)
        anonymous_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(Invalid_Input):
        expected_customer = Customers(first_name='test', last_name='testo', address='hgosrim 45',
                                      phone_number='test0528795548', credit_card_number='test38748593', user_id=3)
        expected_user = Customers(first_name='test', last_name='testo', address='hgosrim 45',
                                  phone_number='test0528795548', credit_card_number='test38748593', user_id=3)
        anonymous_facade_object.add_customer(expected_customer, expected_user)
