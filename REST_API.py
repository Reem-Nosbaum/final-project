from flask import Flask, request
import json
from db_repo import DbRepo
from db_config import local_session
from tabels.Customers import Customers
from tabels.Users import Users

repo = DbRepo(local_session)
app = Flask(__name__)


def convert_to_json(_list):
    json_list = []
    for i in _list:
        _dict = i.__dict__
        _dict.pop('_sa_instance_state', None)
        json_list.append(_dict)
    return json_list


@app.route("/")
def home():
    print('hi')
    return '''
        <html>
            Customers!
            Countries!
            Administrators!
            Airline Companies!
            Users!
            User-Roles!
            Flights!
            Tickets!
        </html>
    '''


@app.route('/customers', methods=['GET', 'POST'])
def get_or_post_customer():
    if request.method == 'GET': return json.dumps(convert_to_json(repo.get_all(Customers)))
    if request.method == 'POST':
        new_customer = request.get_json()
        repo.add(Users(     id=new_customer['user_id'],
                            username=new_customer['username'],
                            password=new_customer['password'],
                            email=new_customer['email'],
                            user_role=3))
        repo.add(Customers( id=new_customer['id'],
                            first_name=new_customer['first_name'],
                            last_name=new_customer['last_name'],
                            address=new_customer['address'],
                            phone_number=new_customer['phone_number'],
                            credit_card_number=new_customer['credit_card_number'],
                            user_id=new_customer['user_id']))
        return '{"status": "success"}'


@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def get_customer_by_id(id):
    if request.method == 'GET':
        for c in convert_to_json(repo.get_all(Customers)):
            if c["id"] == id:
                return json.dumps(c)
        return '{}'
    if request.method == 'PUT':
        updated_new_customer = request.get_json()
        customers_json = convert_to_json(repo.get_all(Customers))
        for c in customers_json:
            if c["id"] == id:
                c["id"] = updated_new_customer["id"] if "id" in updated_new_customer.keys() else None
                c["first_name"] = updated_new_customer["first_name"] if "first_name" in updated_new_customer.keys() else None
                c["last_name"] = updated_new_customer["last_name"] if "last_name" in updated_new_customer.keys() else None
                c["address"] = updated_new_customer["address"] if "address" in updated_new_customer.keys() else None
                c["phone_number"] = updated_new_customer["phone_number"] if "phone_number" in updated_new_customer.keys() else None
                c["credit_card_number"] = updated_new_customer["credit_card_number"] if "credit_card_number" in updated_new_customer.keys() else None
                repo.update_by_id(Customers, Customers.id, id, c)
                return json.dumps(updated_new_customer)
            repo.add(Users(     id=updated_new_customer['user_id'],
                                username=updated_new_customer['username'],
                                password=updated_new_customer['password'],
                                email=updated_new_customer['email'],
                                user_role=3))
            repo.add(Customers( id=updated_new_customer['id'],
                                first_name=updated_new_customer['first_name'],
                                last_name=updated_new_customer['last_name'],
                                address=updated_new_customer['address'],
                                phone_number=updated_new_customer['phone_number'],
                                credit_card_number=updated_new_customer['credit_card_number'],
                                user_id=updated_new_customer['user_id']))
            return '{"status": "success"}'
    if request.method == 'PATCH':
        updated_customer = request.get_json()
        customers_json = convert_to_json(repo.get_all(Customers))
        for c in customers_json:
            if c["id"] == id:
                c["id"] = updated_customer["id"] if "id" in updated_customer.keys() else None
                c["first_name"] = updated_customer["first_name"] if "first_name" in updated_customer.keys() else None
                c["last_name"] = updated_customer["last_name"] if "last_name" in updated_customer.keys() else None
                c["address"] = updated_customer["address"] if "address" in updated_customer.keys() else None
                c["phone_number"] = updated_customer["phone_number"] if "phone_number" in updated_customer.keys() else None
                c["credit_card_number"] = updated_customer["credit_card_number"] if "credit_card_number" in updated_customer.keys() else None
                repo.update_by_id(Customers, Customers.id, id, c)
                return '{"status": "success"}'
        return '{"status": "not found"}'
    if request.method == 'DELETE':
        deleted_customer = request.get_json()
        customers_json = convert_to_json(repo.get_all(Customers))
        for c in customers_json:
            if c["id"] == id:
                repo.delete_by_id(Customers, Customers.id, id)
                repo.delete_by_id(Users, Users.id, c["user_id"])
        return f'{json.dumps(deleted_customer)} deleted'
    return '{"status": "not found"}'

app.run()
