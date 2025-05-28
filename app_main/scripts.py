known_cities = ['Istanbul']

def extract_city_from_list(address):
    for city in known_cities:
        if city.lower() in address.lower():
            return city
        return None