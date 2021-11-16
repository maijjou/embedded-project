from flask import Response, request
from database.models import Route, Tag, User
from flask_restful import Resource

class RouteApi(Resource):
    def put(self, id):
        body = request.get_json() 
        Route.objects.get(id=id).update(**body)
        return '', 200

    def get(self, id):
        routes = Route.objects.get(id=id).to_json()
        return Response(routes, mimetype="application/json", status=200)

class TagApi(Resource):
    def put(self, id):
        print("here {}".format(id))
        body = request.get_json()
        tag = Tag.objects(tag_id=id)
        route_id = tag.id
        Route(id=route_id).update(**body)

        return '', 200

    def post(self, id):
        body = request.get_json()
        tag = Tag.objects.get(tag_id=id)
        print(str(tag.tag_id))
        route = Route(**body).save()
        route_ref_id = route.to_dbref()
        tag.routes.append(route_ref_id)
        tag.save()

        return {'id': str(route.id)}, 200
    
    def get(self, id):
        tag = Tag.objects(tag_id=id).to_json()
        return Response(tag, mimetype="application/json", status=200)

class LeaderTagApi(Resource):
    def get(self, leader_id): 
        leader_data = User.objects.get(leader_id=leader_id)
        req_id = leader_data.current_tag
        tag = Tag.objects.get(tag_id=req_id).to_json()
        return Response(tag, mimetype="application/json", status=200)

    def put(self, id):
        body = request.get_json()
        User.objects.get(id=id).update(**body)
    