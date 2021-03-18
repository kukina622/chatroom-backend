from flask import Flask, Blueprint
from flask_restful import Api
from .user import login,register,logout,search,foo

api_bp=Blueprint("api",__name__)

api=Api(api_bp)

api.add_resource(login,"/login")
api.add_resource(register,"/register")
api.add_resource(logout,"/logout")
api.add_resource(search,"/search/<string:searchUsername>")
api.add_resource(foo,"/foo")