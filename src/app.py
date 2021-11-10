from flask import Flask, Response, request, make_response, jsonify
try:
    from controllers.user_controller import UserController
    from exceptions.user_exception import UserException
except ModuleNotFoundError:
    from src.controllers.user_controller import UserController
    from src.exceptions.user_exception import UserException

app = Flask(__name__)
user_controller = UserController()


@app.route("/users", methods=['POST', 'DELETE'])
def user_management() -> Response:
    try:
        if request.method == 'POST':
            return jsonify(user_controller.store_user(request.json))
        if request.method == 'DELETE':
            return jsonify(user_controller.delete_all_users())
    except Exception as ue:
        if ue.error == UserException.USER_EXISTS:
            return make_response(jsonify(ue.error), 500)
        if ue.error == UserException.PASSWORD_ILLEGAL or \
                ue.error == UserException.ROLE_INVALID or \
                ue.error == UserException.EMAIL_INVALID or \
                ue.error == UserException.NAME_INVALID or \
                ue.error == UserException.EMPTY_NAME:
            return make_response(jsonify(ue.error), 400)


@app.route("/users/<email>", methods=['PUT', 'GET'])
def users(email: str) -> Response:
    try:
        if request.method == 'PUT':
            return jsonify(
                user_controller.update_user(
                    email=email,
                    details=request.json
                )
            )
        if request.method == 'GET':
            return jsonify(user_controller.get_user(email=email))
    except Exception as ue:
        if ue.error == UserException.NO_USER:
            return make_response(jsonify(ue.error), 404)


@app.route("/users/login/<email>", methods=['GET'])
# Todo Get password from query parameters
def login(email: str) -> Response:
    try:
        password = request.args.get('password', None)
        if not password:
            raise UserException(UserException.NO_PASSWORD)
        return jsonify(user_controller.login(email, password))
    except Exception as ue:
        if ue.error == UserException.NO_PASSWORD:
            return make_response(jsonify(ue.error), 400)
        if ue.error == UserException.NO_USER:
            return make_response(jsonify(ue.error), 404)
        if ue.error == UserException.LOGIN_FAILED:
            return make_response(jsonify(ue.error), 401)


@app.route("/users/search", methods=['GET'])
# Todo Get All relevant parameters from query parameters
def search() -> Response:
    try:
        size = int(request.args.get('size', 3))
        page = int(request.args.get('page', 1))
        sort_by = request.args.get('sortBy', None)
        sort_order = request.args.get('sortOrder', None)
        criteria_type = request.args.get('criteriaType', None)
        criteria_value = request.args.get('criteriaValue', None)
        unordered_users = user_controller.get_all_users()
        user_controller.prepare_user_dates(unordered_users)
        ordered_users = user_controller.get_users_ordered(
            users=unordered_users,
            sort_by=sort_by,
            sort_order=sort_order
        )
        if criteria_type and criteria_value:
            ordered_users = user_controller.search_users(
                users=ordered_users,
                criteria_type=criteria_type,
                criteria_value=criteria_value
            )
        user_controller.convert_user_dates(ordered_users)
        return jsonify(_paginate(ordered_users, page, size))
    except Exception as ex:
        make_response(jsonify('Error: No routing implemented'), 404)


def _paginate(users_list: list[dict], pages: int, size: int) -> list[list]:
    return_list = []
    for list_index in range(pages):
        if not len(users_list):
            break
        return_list.append([])
        while len(return_list[list_index]) < size and len(users_list):
            return_list[list_index].append(users_list.pop(0))
    return return_list


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
