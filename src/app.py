from flask import Flask, Response, request, make_response, jsonify

app = Flask(__name__)


@app.route("/users", methods=['POST', 'DELETE'])
def user_management() -> Response:
    try:
        if request.method == 'POST':
            return jsonify({})
        if request.method == 'DELETE':
            return jsonify({})

    except Exception as ex:
        return make_response(jsonify('Error: No routing implemented'), 404)


@app.route("/users/<email>", methods=['PUT', 'GET'])
def users(email: str) -> Response:
    try:
        if request.method == 'PUT':
            return jsonify({})
        if request.method == 'GET':
            return jsonify({})

    except Exception as ex:
        make_response(jsonify('Error: No routing implemented'), 404)


@app.route("/users/login/<email>", methods=['GET'])
# Todo Get password from query parameters
def login(email: str) -> Response:
    try:
        return jsonify({})

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
    app.run(debug=True, threaded=True, port=5000)
