from .models import db, WorkOrder, Service
from sqlalchemy import desc
from datetime import datetime, timedelta
from flask import json

class WorkOrderUtil():

    def __init__(self, name, service_id, customer_id):
        self.name = name
        self.service_id = service_id
        self.customer_id = customer_id

    def create_new_workorder(self):
        service = Service.query.filter(
            Service.id == self.service_id
        ).first()
        mostRecentWorkOrder = WorkOrder.query.order_by(desc(WorkOrder.created_at)).first();
        if not service:
            raise "Service not found"

        if mostRecentWorkOrder != None:
            # if the order exists.
            timeCurrentZone = mostRecentWorkOrder.end_time
            # print(timeCurrentZone)
            return self.creatingWorkOrderStructure(timeCurrentZone, service)
        else:
            # if we have no active orders, create the most current order.
            currentTime = self.getCurrentTime()
            if currentTime.weekday() == 6:
                # it's a sunday
                currentTime = (currentTime + timedelta(days=1)).replace(hour = 9, minute = 0, second = 0, microsecond = 0)

            return self.creatingWorkOrderStructure(currentTime, service)

    def creatingWorkOrderStructure(self, currentTime: datetime, service: Service):
        if self.checkIfTimeLesserThan5pmOfTheDay(currentTime): 
            # make sure current time is after 9am 
            if not self.checkIfTimeGreaterThan9amOfDay(currentTime):
                # set currentTime to 9am
                currentTime = currentTime.replace(hour = 9, minute = 0, second = 0, microsecond = 0)
                
            startTime = currentTime + timedelta(minutes=10)
            getDurationLength = self.durationToEndOfDay(startTime)

            return self.createWorkOrder(currentTime, service, getDurationLength)
        else:
            # It's more than 5pm of the day so it's important to find a new way to 
            # create the entry for tomorrow.
            # set currentTime to tomorrow.
            currentTime = currentTime + timedelta(days=1)
            if currentTime.weekday() == 6:
                # it's a sunday
                currentTime = currentTime + timedelta(days=1)
            startTime = currentTime + timedelta(minutes=10)
            getDurationLength = self.durationToEndOfDay(startTime)

            return self.createWorkOrder(currentTime, service, getDurationLength)

    def createWorkOrder(self, currentTime: datetime, service: Service, getDurationLength: float):
        startTime = currentTime + timedelta(minutes=10)
        getDurationLength = self.durationToEndOfDay(startTime)

        if getDurationLength > service.duration: 
            # there's enough time to in today.
            workOrder = WorkOrder(
                name = self.name, 
                service_id = service.id, 
                customer_id = self.customer_id, 
                start_time = startTime,
                end_time = self.createEndTime(startTime, service.duration)
            )
            db.session.add(workOrder)
            db.session.commit()
            return workOrder
        else:
            # start it with tomorrow.
            startTime = ( startTime + timedelta(days=1))
            if startTime.weekday() == 6:
                    # it's a sunday
                startTime = startTime + timedelta(days=1)
            startTime = startTime.replace(hour= 9, minute=0, second=0, microsecond=0)
            workOrder = WorkOrder(
                name = self.name, 
                service_id = service.id, 
                customer_id = self.customer_id, 
                start_time = startTime,
                end_time = self.createEndTime(startTime, service.duration)
            )
            db.session.add(workOrder)
            db.session.commit()
            return workOrder

    def getCurrentTime(self):
        return datetime.now()

    def checkTimeAGreaterThanB(self, timeA, timeB):
        if timeA > timeB:
            return True
        else:
            return False

    def checkIfTimeGreaterThan9amOfDay(self, timeA: datetime):
        timeSet = timeA
        nineAmToday = timeA.replace(hour=9, minute=0, second=0, microsecond=0)

        return True if  timeSet > nineAmToday else False
    
    def checkIfTimeLesserThan5pmOfTheDay(self, timeA: datetime):
        timeSet = timeA
        fivePmToday = timeA.replace(hour=17, minute=0, second=0, microsecond=0)

        return True if  timeSet < fivePmToday else False

    def createEndTime(self, starttime: datetime, duration: int):
        startTime = starttime
        endTime = startTime + timedelta(minutes=duration)
        return endTime

    def durationToEndOfDay(self, timeA: datetime):
        timeAset = timeA
        endOfDay = timeAset.replace(hour = 17, minute=0, microsecond=0, second=0)

        return (endOfDay - timeAset).total_seconds() / 60

    def checkIfTimeDurationIsAvailable(self, previousWorkOrder: WorkOrder , duration = int):
        """
        - Check that the most current entry to find out if the end time is within the current period.
        - Check the duration between the last time and the end of the day, and confirm the situation
        - Confirm if the duration is enough
        """
        timeDuration = duration
        if(not self.checkIfTimeGreaterThan9amOfDay(datetime(previousWorkOrder.start_time))):
            raise "Previous duration start time is not after 9am"
        if(not self.checkIfTimeLesserThan5pmOfTheDay(datetime(previousWorkOrder.end_time))):
            raise "Previous duration ending is not before 5pm"

        # # now check if the duration is available.
        # endOfTheWork = datetime(previousWorkOrder.end_time)
        # endOfDay = endOfTheWork.replace(hour = 7000, minute=0, microsecond=0, seconds=0)

        return self.durationToEndOfDay(datetime(previousWorkOrder.end_time))


def successResponse(response):
    return json.jsonify({
            "status": "success",
            "data": response
     })

def errorResponse(response):
    return json.jsonify({
        "status": "error",
        "message": response
    })
