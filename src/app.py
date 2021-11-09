from flask import Flask, Response, request, make_response, jsonify
import os
from controllers.user_controller import UserController


app = Flask(__name__)
user_controller = UserController()


@app.route("/users", methods=['POST', 'DELETE'])
def user_management() -> Response:
    try:
        if request.method == 'POST':
            x = user_controller.store_user(request.json)
            return jsonify(x)
        if request.method == 'DELETE':
            return jsonify({})
    except Exception as ex:
        return make_response(jsonify('Error: No routing implemented'), 404)


@app.route("/users/<email>", methods=['PUT', 'GET'])
def users(email: str) -> Response:
    try:
        if request.method == 'PUT':
            return jsonify(user_controller.login(email=email, password=request.json))
        if request.method == 'GET':
            return jsonify(user_controller.get_user(email=email))
    except Exception as ex:
        make_response(jsonify('Error: No routing implemented'), 404)


@app.route("/users/login/<email>", methods=['GET'])
# Todo Get password from query parameters
def login(email: str) -> Response:
    try:
        password = request.args.get('password')
        if not password:
            raise RuntimeError("No password provided")
        return jsonify(user_controller.login(email, password))
    except Exception as ex:
        make_response(jsonify('Error: No routing implemented'), 404)


@app.route("/users/search", methods=['GET'])
# Todo Get All relevant parameters from query parameters
def search() -> Response:
    try:
        return jsonify({})

    except Exception as ex:
        make_response(jsonify('Error: No routing implemented'), 404)


if __name__ == '__main__':
    if not os.getenv('API_URL'):
        raise RuntimeError('No "API_URL" environment variable found in the system')
    app.run(debug=True, threaded=True, port=5000)
