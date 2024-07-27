import requests 

from models import db, Person, Film, Starship, Vehicle, Species, Planet

BASE_URL = "https://swapi.dev/api/"


def fetch_and_store_people():
    """Get json response of API data for People"""
    url = f'{BASE_URL}people/'

    while url:
        res = requests.get(url)
        data = res.json()

        for item in data['results']:
            homeworld_id = None
            if item['homeworld']:
                homeworld_id = int(item['homeworld'].split('/')[-2])

            person = Person(
                name=item['name'],
                birth_year=item['birth_year'],
                eye_color=item['eye_color'],
                gender=item['gender'],
                hair_color=item['hair_color'],
                height=item['height'],
                mass=item['mass'],
                skin_color=item['skin_color'],
                homeworld_id=homeworld_id,
            )
            db.session.add(person)
            db.session.commit()

            for film_url in item['films']:
                film_id = int(film_url.split('/')[-2])
                film = Film.query.get(film_id)
                if film:
                    person.films.append(film)

            for species_url in item['species']:
                species_id = int(species_url.split('/')[-2])
                species = Species.query.get(species_id)
                if species:
                    person.species.append(species)

            for starship_url in item['starships']:
                starship_id = int(starship_url.split('/')[-2])
                starship = Starship.query.get(starship_id)
                if starship:
                    person.starships.append(starship)

            for vehicle_url in item['vehicles']:
                vehicle_id = int(vehicle_url.split('/')[-2])
                vehicle = Vehicle.query.get(vehicle_id)
                if vehicle:
                    person.vehicles.append(vehicle)


        db.session.commit()

        url = data['next']



def fetch_and_store_films():
    """Get json response of API data for Films"""
    url = f'{BASE_URL}films/'

    while url:
        res = requests.get(url)
        data = res.json()

        for item in data['results']:
            film = Film(
                title=item['title'],
                episode_id=item['episode_id'],
                opening_crawl=item['opening_crawl'],
                director=item['director'],
                producer=item['producer'],
                release_date=item['release_date'],
            )
            db.session.add(film)
            db.session.commit()

            for species_url in item['species']:
                species_id = int(species_url.split('/')[-2])
                species = Species.query.get(species_id)
                if species:
                    film.species.append(species)

            for starship_url in item['starships']:
                starship_id = int(starship_url.split('/')[-2])
                starship = Starship.query.get(starship_id)
                if starship:
                    film.starships.append(starship)

            for vehicle_url in item['vehicles']:
                vehicle_id = int(vehicle_url.split('/')[-2])
                vehicle = Vehicle.query.get(vehicle_id)
                if vehicle:
                    film.vehicles.append(vehicle)
            
            for person_url in item['characters']:
                person_id = int(person_url.split('/')[-2])
                person = Person.query.get(person_id)
                if person:
                    film.characters.append(person)

            for planet_url in item['planets']:
                planet_id = int(planet_url.split('/')[-2])
                planet = Planet.query.get(planet_id)
                if planet:
                    film.planets.append(planet)

            db.session.commit()

        url= data['next']



def fetch_and_store_starships():
    """Get json response of API data for Starships"""
    url = f'{BASE_URL}starships/'

    while url:
        res = requests.get(url)
        data = res.json()


        for item in data['results']:
            starship = Starship(
                name=item['name'],
                model=item['model'],
                starship_class=item['starship_class'],
                manufacturer=item['manufacturer'],
                cost_in_credits=item['cost_in_credits'],
                length=item['length'],
                crew=item['crew'],
                passengers=item['passengers'],
                max_atmosphering_speed=item['max_atmosphering_speed'],
                hyperdrive_rating=item['hyperdrive_rating'],
                MGLT=item['MGLT'],
                cargo_capacity=item['cargo_capacity'],
                consumables=item['consumables'],
            )
            db.session.add(starship)
            db.session.commit()

            for film_url in item['films']:
                film_id = int(film_url.split('/')[-2])
                film = Film.query.get(film_id)
                if film:
                    starship.films.append(film)

            for person_url in item['pilots']:
                person_id = int(person_url.split('/')[-2])
                pilot = Person.query.get(person_id)
                if pilot:
                    starship.pilots.append(pilot)
            
            db.session.commit()

        url= data['next']



def fetch_and_store_vehicles():
    """Get json response of API data for Vehicles"""
    url = f'{BASE_URL}vehicles/'

    while url:
        res = requests.get(url)
        data = res.json()

        for item in data['results']:
            vehicle = Vehicle(
                name=item['name'],
                model=item['model'],
                vehicle_class=item['vehicle_class'],
                manufacturer=item['manufacturer'],
                length=item['length'],
                cost_in_credits=item['cost_in_credits'],
                crew=item['crew'],
                passengers=item['passengers'],
                max_atmosphering_speed=item['max_atmosphering_speed'],
                cargo_capacity=item['cargo_capacity'],
                consumables=item['consumables'],
            )
            db.session.add(vehicle)
            db.session.commit()

            for film_url in item['films']:
                film_id = int(film_url.split('/')[-2])
                film = Film.query.get(film_id)
                if film:
                    vehicle.films.append(film)

            for person_url in item['pilots']:
                person_id = int(person_url.split('/')[-2])
                pilot = Person.query.get(person_id)
                if pilot:
                    vehicle.pilots.append(pilot)
            
            db.session.commit()

        url= data['next']




def fetch_and_store_species():
    """Get json response of API data for Species"""
    url = f'{BASE_URL}species/'

    while url:
        res = requests.get(url)
        data = res.json()

        for item in data['results']:
            homeworld_url = item.get('homeworld')
            if homeworld_url:
                homeworld_id = int(item['homeworld'].split('/')[-2])
            else:
                homeworld_id = None

            species = Species(
                name=item['name'],
                classification=item['classification'],
                designation=item['designation'],
                average_height=item['average_height'],
                average_lifespan=item['average_lifespan'],
                eye_colors=item['eye_colors'],
                hair_colors=item['hair_colors'],
                skin_colors=item['skin_colors'],
                language=item['language'],
                homeworld_id=homeworld_id,
            )
            db.session.add(species)
            db.session.commit()

            for film_url in item['films']:
                film_id = int(film_url.split('/')[-2])
                film = Film.query.get(film_id)
                if film:
                    species.films.append(film)

            for person_url in item['people']:
                person_id = int(person_url.split('/')[-2])
                person = Person.query.get(person_id)
                if person:
                    species.people.append(person)
        
            db.session.commit()

        url= data['next']




def fetch_and_store_planets():
    """Get json response of API data for Planets"""
    url = f'{BASE_URL}planets/'

    while url:
        res = requests.get(url)
        data = res.json()

        for item in data['results']:
            planet = Planet(
                name=item['name'],
                diameter=item['diameter'],
                rotation_period=item['rotation_period'],
                orbital_period=item['orbital_period'],
                gravity=item['gravity'],
                population=item['population'],
                climate=item['climate'],
                terrain=item['terrain'],
                surface_water=item['surface_water'],
            )
            db.session.add(planet)
            db.session.commit()


            for film_url in item['films']:
                film_id = int(film_url.split('/')[-2])
                film = Film.query.get(film_id)
                if film:
                    planet.films.append(film)

            for person_url in item['residents']:
                person_id = int(person_url.split('/')[-2])
                person = Person.query.get(person_id)
                if person:
                    planet.residents.append(person)
        
            db.session.commit()

        url= data['next']


def fetch_all_data():
    """Fetch all data from SWAPI and store in the database"""
    fetch_and_store_planets()
    fetch_and_store_people()
    fetch_and_store_films()
    fetch_and_store_species()
    fetch_and_store_starships()
    fetch_and_store_vehicles()
    
