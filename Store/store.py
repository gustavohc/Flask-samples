from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My_Store',
        'items': [
            {
                'name': 'My_item',
                'price': 15.99
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    for s in stores:
        if s['name'] == name:
            return jsonify(s)
    return jsonify({'message' : 'store not found'})

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stories':stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    request_data = request.get_json()
    for s in stores:
        if s['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            s['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message' : 'store not found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for s in stores:
        if s['name'] == name:
            return jsonify(s['items'])
    return jsonify({'message' : 'store not found'})

app.run(port=5000)
