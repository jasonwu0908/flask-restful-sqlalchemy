import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.secret_key = 'jose' # app.config['JWT_SECRET_KEY']

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)
db.init_app(app)
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claim_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}



api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
