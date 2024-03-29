from flask_restful import Resource
from models.store import Store

class StoreResources(Resource):
    def get(self, name):
        store = Store.find_by_name(name)
        if store:
            return store.json()
        return {"message": 'Store not found'}, 404

    def post(self, name):
        if Store.find_by_name(name):
            return {'message': "A store with name {} already exists".format(name)}, 400

        store = Store(name)

        try:
            store.save_to_db()
        except:
            return {'message': "An error accurred while creating the store"}, 500

        return store.json(), 201

    def delete(self, name):
        store = Store.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted!'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in Store.find_all()]}
