from flask import Flask, request, make_response, jsonify
from configparser import ConfigParser
from db_repo_pool import DbRepoPool
from facade.Anonymous_Facade import AnonymousFacade
from tables.Customers import Customers
from tables.Users import Users
from flask_cors import CORS
config = ConfigParser()
config.read('config.conf')
repool = DbRepoPool.get_instance()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
	return make_response(jsonify({'page': 'home'}), 200)


@app.route('/login', methods=['POST'])
def login():
	repo = repool.get_connection()
	anon_facade = AnonymousFacade(repo)
	request_body = request.get_json()
	username = request_body["username"]
	password = request_body["password"]
	anon_facade.login(username=username, password=password)
	repool.return_connection(repo)
	return make_response(jsonify({'status': 'success'}), 200)



@app.route('/signup', methods=['POST'])  # add customer
def signup():
	repo = repool.get_connection()
	anon_facade = AnonymousFacade(repo)
	request_body = request.get_json()
	username = request_body['username']
	password = request_body['password']
	email = request_body['email']
	new_user = Users(username=username, password=password, email=email, user_role=3)
	first_name = request_body['first_name']
	last_name = request_body['last_name']
	address = request_body['address']
	phone_number = request_body['phone_number']
	credit_card_number = request_body['credit_card_number']
	new_customer = Customers(first_name=first_name, last_name=last_name, address=address, phone_number=phone_number, credit_card_number=credit_card_number )
	anon_facade.add_customer(customer=new_customer, user=new_user)
	repool.return_connection(repo)
	return make_response(jsonify({'task': 'signup', 'status': 'success'}), 200)


@app.route('/flights')  # get all flights, get flights by params, by airline
def flights():
	#need to add query params
	repo = repool.get_connection()
	anon_facade = AnonymousFacade(repo)
	flights_ = anon_facade.get_all_flights()
	repool.return_connection(repo)
	json_flights = [flight.data_for_web() for flight in flights_]
	return jsonify(json_flights)


@app.route('/flights/<int:id_>')  # get flight by id
def flight_by_id(id_):
	repo = repool.get_connection()
	anon_facade = AnonymousFacade(repo)
	flight_id = anon_facade.get_flight_by_id(id=id_)
	repool.return_connection(repo)
	json_flight_id = flight_id.data_for_web()
	return jsonify(json_flight_id)


@app.route('/countries')  # get all countries
def countries():
	repo = repool.get_connection()
	anon_facade = AnonymousFacade(repo)
	countries_ = anon_facade.get_all_countries()
	repool.return_connection(repo)
	json_countries = [country.get_dictionary() for country in countries_]
	return jsonify(json_countries)


@app.route('/countries/<int:id_>')  # get country by id
def country_by_id(id_):
	repo = repool.get_connection()
	anon_facade = AnonymousFacade(repo)
	country_id = anon_facade.get_country_by_id(id=id_)
	repool.return_connection(repo)
	json_country_id = [country_id.get_dictionary()]
	return jsonify(json_country_id)


@app.route('/airlines')  # get all airlines
def airlines():
	repo = repool.get_connection()
	anon_facade = AnonymousFacade(repo)
	airlines_ = anon_facade.get_all_airlines()
	repool.return_connection(repo)
	json_airlines = [airline.get_dictionary() for airline in airlines_]
	return jsonify(json_airlines)


@app.route('/airlines/<int:id_>')  # get airline by id
def airline_by_id(id_):
	repo = repool.get_connection()
	anon_facade = AnonymousFacade(repo)
	airline_id = anon_facade.get_airline_by_id(id=id_)
	repool.return_connection(repo)
	json_airline_id = airline_id.get_dictionary()
	return jsonify(json_airline_id)


if __name__ == '__main__':
	app.run(debug=True)
