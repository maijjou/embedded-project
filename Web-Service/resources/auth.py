from flask import request, Response
from database.models import User
from flask_restful import Resource
import random

class SignUpApi(Resource):
    def post(self): 
        body = request.get_json()
        print(body)
        user = User(**body)
        user.hash_password()
        user.leader_id = random.randrange(1000, 9999)
        user.save()
        id = user.id

        return {'id': str(id)}, 200
        
class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email= body.get('email'))
        authorized = user.check_password(body.get('password'))

        if not authorized:
            return { 'error': 'Email or password invalid'}, 401 

        print(user.to_json())
        
        return user.to_json()
