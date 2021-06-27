from .models import db, WorkOrder, Service
from sqlalchemy import desc

class WorkOrderUtil():

    def __init__(self, name, service_id, start_date, end_date, customer_id):
        self.name = name
        self.service_id = service_id

    def create_new(self):
        service = Service.query.filter(
            Service.id == self.service_id
        ).first()
        mostRecentWorOrder = WorkOrder.query.order_by(desc(WorkOrder.created_at)).first();
        # Create a new work Order from the request object
