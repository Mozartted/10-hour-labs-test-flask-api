"""Application routes."""
from datetime import datetime as dt
from .util import WorkOrderUtil
from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for, jsonify, json

from .models import Customer, Service, WorkOrder, db, ServiceSchema


service_schema = ServiceSchema()
# @app.route("/", methods=["GET"])
# def user_records():
#     """Create a user via query string parameters."""
#     username = request.args.get("user")
#     email = request.args.get("email")
#     if username and email:
#         existing_user = User.query.filter(
#             User.username == username or User.email == email
#         ).first()
#         if existing_user:
#             return make_response(f"{username} ({email}) already created!")
#         new_user = User(
#             username=username,
#             email=email,
#             created=dt.now(),
#             bio="In West Philadelphia born and raised, \
#             on the playground is where I spent most of my days",
#             admin=False,
#         )  # Create an instance of the User class
#         db.session.add(new_user)  # Adds new User record to database
#         db.session.commit()  # Commits all changes
#         redirect(url_for("user_records"))
#     return render_template("users.jinja2", users=User.query.all(), title="Show Users")
@app.route('/', methods=["GET"])
def welcome():
    return jsonify({'response': "Welcome"});


@app.route("/services", methods=["GET"])
def services():
    services = Service.query.all()
    # for service in services:
    #     print(service.name)
    return json.jsonify(service_schema.dump(services))

@app.route('/create', methods=["POST"])
def create_order():
    workOrderObject = request.get_json()
    # return workOrderObject["some"]
    workResponse = WorkOrderUtil(name=workOrderObject["name"], service_id=workOrderObject['service_id'])

    return workResponse
# @app.route('/order',methods=['POST'])
# def create_order():
#     body = request.
