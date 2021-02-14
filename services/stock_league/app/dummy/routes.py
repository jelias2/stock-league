from flask import Blueprint, request, jsonify
from os.path import realpath, dirname

import firebase_admin
from firebase_admin import credentials, firestore, initialize_app


if not firebase_admin._apps:
    dir_path = dirname(dirname(realpath(__file__)))
    cred = credentials.Certificate(f"{dir_path}/firebase_credentials/service_account_key.json")
    firebase_app = initialize_app(cred)


routes_blueprint = Blueprint('routes', __name__, url_prefix="/routes")


db = firestore.client()
todos = db.collection("todos")


@routes_blueprint.route('/')
@routes_blueprint.route('/home')
def index():
    return "<h1>Stock League</h1>"


@routes_blueprint.route("/add", methods=["POST"])
def create():
    """
        create(): Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request,
    """
    try:
        data = request.get_json()
        id = data.get('id')
        todos.document(str(id)).set(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 500


@routes_blueprint.route("/list", methods=["GET"])
def read():
    """
        read(): Fetches documentd from Firestore collection as JSON
        todo: Return document that matches query ID.
        all_todos: Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = todos.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todos.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@routes_blueprint.route('/update', methods=["POST", "PUT"])
def update():
    """
        update(): Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json.get('id')
        todos.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@routes_blueprint.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete(): Delete a document from Firestore collection
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todos.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
