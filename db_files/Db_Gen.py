import json


#def generate_countries():
#    with open(r"db_files/countries_j.json") as c:
#        json.load(c)
#    print(c)

generate_countries()


def generate_countries():
    countries_ls = []
    with open(r"countries_j.json.json") as f:
        countries = json.load(f)
    for country in countries:
        countries_ls.append(countries(name=country['name']))
    print(countries_ls)


generate_countries()
