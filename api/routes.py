"""Application routes."""
from datetime import datetime as dt
import sys
from .util import WorkOrderUtil, successResponse, errorResponse
from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for, jsonify, json
from .models import Customer, Service, WorkOrder, db, ServiceSchema, WorkOrderSchema, CustomerSchema


service_schema = ServiceSchema(many=True)
work_schema = WorkOrderSchema()
work_schema_list = WorkOrderSchema(many=True)
customer_schema = CustomerSchema(many = True)
customer_schema_list = CustomerSchema()

@app.route('/', methods=["GET"])
def welcome():
    return jsonify({'response': "Welcome"});

@app.route("/services", methods=["GET"])
def services():
    services = Service.query.all()
    return successResponse(service_schema.dump(services))

@app.route("/customers", methods=["GET"])
def customers():
    customers = Customer.query.all()
    return successResponse(customer_schema.dump(customers))

@app.route("/customer/create", methods=["POST"])
def customerCreate():
    try:
        customerObject = request.get_json()
        customer = Customer(username=customerObject['username'], email=customerObject['email'])
        db.session.add(customer)
        db.session.commit()

        return successResponse(customer_schema_list.dump(customer))

    except Exception as e:
        return errorResponse(str(e))

@app.route('/workorder/create', methods=["POST"])
def create_order():
    # try:
    workOrderObject = request.get_json()
    customerId = request.headers.get("customer_id")
    # return workOrderObject["some"]
    if  customerId != None:
        workUtil = WorkOrderUtil(
            name=workOrderObject["name"], 
            service_id=workOrderObject['service_id'], 
            customer_id=customerId
        )
        workResponse = workUtil.create_new_workorder()
        return successResponse(work_schema.dump(workResponse))
    else:
        return errorResponse("Customer header not present")


@app.route('/workorders', methods=["GET"])
def get_orders():
    customerId = request.headers.get("customer_id")
    if  customerId != None:
        try:
            if customerId:
                workResponses = WorkOrder.query.filter( WorkOrder.customer_id == customerId).order_by("created_at")
                return successResponse(work_schema_list.dump(workResponses))
            else:
                return errorResponse("Add the customer id")
        except:
            return errorResponse(sys.exc_info()[0])
    else:
        return errorResponse("Customer header not present")
