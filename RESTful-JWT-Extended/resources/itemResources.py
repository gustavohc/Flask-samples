from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    jwt_optional,
    fresh_jwt_required
    )
from models.item import Item

class ItemResources(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required
    def get(self, name):
        item = Item.find_by_name(name)

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @fresh_jwt_required
    def post(self, name):
        if Item.find_by_name(name):
            return {'message': "An item with name {} already exists".format(name)}, 400 #HTTP bad request
        # data = request.get_json() # force=True: don't need content type header silent=True: return None
        data = ItemResources.parser.parse_args()
        item = Item(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500 # Internal server error

        return item.json(), 201 #HTTP create status

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege.'}, 401

        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deletado'}

    def put(self, name):
        data = ItemResources.parser.parse_args()
        item = Item.find_by_name(name)

        if item is None:
            try:
                item = Item(name, **data)
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {'message': 'An error occurred updating the item.'}, 500

        item.save_to_db()

        return item.json(), 201


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in Item.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }, 200
