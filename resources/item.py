import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, jwt_optional, fresh_jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannnot be left blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")

    @jwt_required
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            {"message": "An error occurred inserting the item"}

        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400  # 400: bad request

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
           item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201  # http code for 'creating' = 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401

        item = ItemModel.find_by_name(name)

        if item:
           item.delete_from_db()
           return {"message": "Item Deleted"}
        return {"message": "Item not found"}, 404



    def put(self,name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)


        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {"message": "An error occurred inserting the item"}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {"message": "An error occurred updating the item"}, 500
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [x.json() for x in ItemModel.find_all()]
        if user_id:
            return {"items": items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }
