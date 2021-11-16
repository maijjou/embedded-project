from enum import unique
from typing import Collection
from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class Stop(db.EmbeddedDocument):
    lat = db.StringField()
    lon = db.StringField()
    location = db.StringField()
    # meta = {'collection': 'Stops'}

class fuel(db.EmbeddedDocument):
    liters = db.StringField()
    arrival_time = db.DateTimeField()  
    departure_time = db.DateTimeField()
    stop = db.EmbeddedDocumentField(Stop)

class maintenance (db.EmbeddedDocument):
    description = db.StringField()
    arrival_time = db.DateTimeField()
    departure_time = db.DateTimeField() 
    stop = db.EmbeddedDocumentField(Stop)
 
class crew_change(db.EmbeddedDocument):
    crew_members = db.ListField()
    arrival_time = db.StringField()
    departure_time = db.StringField()
    stop = db.EmbeddedDocumentField(Stop)
  
class Ship(db.Document):
    crew_change = db.EmbeddedDocumentField(crew_change)
    maintenance = db.EmbeddedDocumentField(maintenance)
    fuel = db.EmbeddedDocumentField(fuel)
    meta = {'collection': 'Ships'}  

class Tour(db.EmbeddedDocument):
    star_time = db.StringField(required=True)
    stop_time = db.StringField(required=True) 
    status = db.StringField(required=True)
 
class Route(db.Document):
    origin = db.StringField(required=True)
    destination = db.StringField(required=True) 
    departure_time = db.StringField(required=True)
    arrival_time = db.StringField(required=True)
    route_status = db.StringField(required=True) # Ongoing, Started
    ship_status = db.ReferenceField('Ship') 
    tour = db.EmbeddedDocumentField(Tour)
    meta = {'collection': 'Routes'}

class Tag(db.Document):
    tag_id = db.IntField(required=True)
    routes = db.ListField(db.ReferenceField('Route'), required=False)
    meta = {'collection': 'Tags'}

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    first_name = db.StringField(required=True)
    last_name = db.StringField(require=True)
    role = db.StringField(required=True)
    leader_id = db.IntField(required=True, unique=True)
    current_tag = db.IntField(required=False)
    meta = {'collection': 'Users'}

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    