from .tour import TagApi, LeaderTagApi, RouteApi
from .auth import SignUpApi, LoginApi


def initialize_routes(api):
    api.add_resource(TagApi, '/api/tag/<id>')
    api.add_resource(LeaderTagApi, '/api/leadertag/<id>', '/api/leadertag/<leader_id>')
    api.add_resource(RouteApi, '/api/route/<id>')
    api.add_resource(SignUpApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')