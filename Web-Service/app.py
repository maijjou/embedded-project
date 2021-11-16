from flask import Flask
from flask_restful import Api 
from datetime import datetime

from database.models import Ship, User, Route, Stop
from database.db import initialize_db
from resources.routes import initialize_routes # This api related not the tour route

app = Flask(__name__)

api = Api(app)

DB_URI = "mongodb+srv://???"
 
app.config["MONGODB_HOST"] = DB_URI

initialize_db(app)
initialize_routes(api)

def test():
    """ This is a test function to checking if the database is working
    """
    usr = User()
    usr.email = "???@gmail.com"
    usr.password = "???"
    usr.first_name = "Jim"
    usr.last_name = "bo"
    usr.role = "Leader"
    
    route = Route()
    route.tag_number = 1

    stop1 = Stop(lat="0.0", lon="1.0", location="Helsinki")
    stop1.save()

    route.origin = str(stop1.id) 
 
    stop2 = Stop(lat="2.0", lon="3.0", location="Turku")
    stop2.save()

    route.destination = str(stop2.id)

    route.arrival_time = datetime.utcnow()
    route.departure_time = datetime.utcnow()
    route.tour_status = "STARTED" 

    ship = Ship()
    ship.save()

    route.ship_status = str(ship.id)

    route.save()

    usr.routes.append( str(route.id))
    usr.save()

if __name__ == "__main__":
    app.run(debug=True)
