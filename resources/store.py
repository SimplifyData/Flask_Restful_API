from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):


    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
        except:
            {"message": "An error occurred inserting the item"}

        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An Store with name '{}' already exists.".format(name)}, 400  # 400: bad request

        store = StoreModel(name)
        try:
           store.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return store.json(), 201  # http code for 'creating' = 201

    def delete(self,name):
        store = StoreModel.find_by_name(name)

        if store:
           store.delete_from_db()

        return {"message": "Store Deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [x.json() for x in StoreModel.find_all()]}
