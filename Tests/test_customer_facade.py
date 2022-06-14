import pytest
from db_config import local_session
from db_files.db_repo import DbRepo
from errors.Invalid_Input import Invalid_Input
from errors.error_no_more_tickets import NoMoreTickets
from errors.error_ticket_not_found import TicketNotFound
from facade.Anonymous_Facade import AnonymousFacade
from facade.Customer_Facade import CustomerFacade
from tables.Customers import Customers
from tables.Tickets import Tickets

repo = DbRepo(local_session)


@pytest.fixture(scope='session')
def customer_facade_object():
    return CustomerFacade(repo)


@pytest.fixture(scope='session')
def customer_token():
    an_facade = AnonymousFacade(repo)
    return an_facade.login('matan89', 'm12312')


@pytest.fixture(scope='function', autouse=True)
def customer_facade_clean():
    repo.reset_db()


def test_update_customer(customer_facade_object, customer_token):
    customer_facade_object.update_customer({'first_name': 'Samuel'}, 2, customer_token)
    check_customer = repo.get_by_id(Customers, 2)
    assert check_customer.first_name == 'Samuel'


def test_not_update_customer(customer_facade_object, customer_token):
    with pytest.raises(Invalid_Input):
        customer_facade_object.update_customer({'first_name': 'Samuel'}, 'uy', customer_token)


def test_add_ticket(customer_facade_object, customer_token):
    customer_facade_object.add_ticket(Tickets(id=999, flight_id=2, customer_id=2), customer_token)
    check_ticket = repo.get_by_id(Tickets, 999)
    assert check_ticket.flight_id == 2
    assert check_ticket.customer_id == 2


def test_not_add_ticket(customer_facade_object, customer_token):
    with pytest.raises(Invalid_Input):
        customer_facade_object.add_ticket('Tickets(flight_id=4, customer_id=1)', customer_token)
    with pytest.raises(NoMoreTickets):
        customer_facade_object.add_ticket(Tickets(flight_id=1, customer_id=1), customer_token)


def test_remove_ticket(customer_facade_object, customer_token):
    customer_facade_object.remove_ticket(2, customer_token)
    check_customer = repo.get_by_id(Tickets, 2)
    assert check_customer is None


def test_not_remove_ticket(customer_facade_object, customer_token):
    with pytest.raises(Invalid_Input):
        customer_facade_object.remove_ticket({'45': '9'}, customer_token)
    with pytest.raises(TicketNotFound):
        customer_facade_object.remove_ticket(45, customer_token)


def test_get_ticket_by_customer(customer_facade_object, customer_token):
    assert repo.get_by_column_value(Tickets, Tickets.customer_id, 2) == customer_facade_object.get_ticket_by_customer(2, customer_token)


def test_not_get_ticket_by_customer(customer_facade_object, customer_token):
    with pytest.raises(Invalid_Input):
        customer_facade_object.get_ticket_by_customer('4', customer_token)

