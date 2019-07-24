import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    connection = False
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)

        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def open_conn(cls):
        cls.connection = sqlite3.connect('data.db')
        return cls.connection.cursor()

    @classmethod
    def close_conn(cls):
        cls.connection.commit()
        cls.connection.close()

    @classmethod
    def find_by_name(cls, name):
        cursor = Item.open_conn()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        Item.close_conn()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        return None

    @classmethod
    def insert_item(cls, item):
        cursor = Item.open_conn()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        Item.close_conn()

    def update_item(cls, item):
        cursor = Item.open_conn()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        Item.close_conn()

    def post(self, name):
        if Item.find_by_name(name):
            return {'message': "An item with name {} already exists".format(name)}, 400 #HTTP bad request
        # data = request.get_json() # force=True: don't need content type header silent=True: return None
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.insert_item(item)
        except:
            return {'message': 'An error occurred inserting the item.'}, 500 # Internal server error

        return item, 201 #HTTP create status

    def delete(self, name):
        item = self.find_by_name(name)
        if item:
            cursor = Item.open_conn()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            Item.close_conn()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found!'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        item_updated = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert_item(item_updated)
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            try:
                self.update_item(item_updated)
            except:
                return {'message': 'An error occurred updating the item.'}, 500
        return item_updated

class ItemList(Resource):
    def get(self):
        cursor = Item.open_conn()
        items = []

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        if result:
            for row in result:
                items.append({'name': row[0], 'price': row[1]})
            return items

        return {'message': 'There is no item in the database!'}
