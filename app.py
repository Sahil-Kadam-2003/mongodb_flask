from flask import Flask, request, jsonify
from flask_pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['myDatabase']


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    users_collection = db['users']
    result = users_collection.find_one({"email":email},{"email":1,"password":1,"name":1})
    if result:
        if password == result.get("password"):
            return jsonify({"message":"user exist","data":[{"email":result.get("email"),"name":result.get("name")}]})
        else:
          return jsonify({"message":"password is correct"})
        
    else:
        return jsonify({"message":"does not exits"})

@app.route("/signup",methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    users_collection = db['users']
    users_collection.insert_one({'email':email,'password':password,'name':name})
    return jsonify({'message':"user registered successfully"})

@app.route("/users",methods=['GET'])
def users():

    email = request.args.get("email")
    users_collection = db['users']
    result = users_collection.find_one({"email":email},{"email":1,"password":1,"name":1})
    if result:
        return jsonify({"message":"user exist","data":[{"name":result.get('name')}]})
    else:
        return jsonify({"message":"user not exist"})

if __name__ == '__main__':
    app.run(debug=True)
