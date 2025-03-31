from connection.database import db
from Models.models import EmployeeModel
from ErrorHandling.errorHandling import clientErrorHandling,serverErrorHandling,successHTTP
from fastapi import HTTPException
import json
from traceback import format_exc

employeeCollection = db['employeeList']

async def createEmployee(emp: EmployeeModel):
    try:
        print("TRY BLOCK EXECUTING")  # Debugging log
        employeeDict = emp.model_dump()
        req_Fields = ['employeeID','firstName','lastName','email']
        miss_Fields = [field for field in req_Fields if not employeeDict.get(field)]
        employeeCheck = await employeeCollection.find_one({"employeeID": employeeDict["employeeID"]})

        if miss_Fields:
            raise clientErrorHandling(400, "Bad Request", f"Missing required fields: {', '.join(miss_Fields)}",emp.model_dump(mode="json"))  
        elif employeeCheck:
            raise clientErrorHandling(409, "Conflict", f"Employee ID {employeeDict['employeeID']} already exists.",emp.model_dump(mode="json"))
            
        employee = await employeeCollection.insert_one(employeeDict)
        if employee.acknowledged:
            print("EMPLOYEE INSERTED SUCCESSFULLY")  
            return successHTTP( "success", f"Employee Information Inserted",emp.model_dump(mode="json"))
        else:
            clientErrorHandling(200,"OK","An Error has been occured on updating information",emp.model_dump(mode="json"))
    except Exception as e:
        raise serverErrorHandling(e)

        
    
async def updateEmployee(id:str,emp: EmployeeModel):
    try:
        employeeDict = emp.model_dump(exclude_unset=True)
        employeeCheck = await employeeCollection.find_one({"employeeID": id}, {"_id": 0})
        if not employeeDict:
            print("EMPTY RESPONSE BODY")  
            raise clientErrorHandling(200,"OK","Response Body is empty",emp.model_dump(mode="json"))
        elif employeeCheck is None:
            raise clientErrorHandling(404,"error",f"Employee ID not Found: {id}",emp.model_dump(mode="json"))
        elif all(employeeDict.get(key) == employeeCheck.get(key) for key in employeeDict):
            print("RECORD ARE THE SAME")  
            raise clientErrorHandling(200,"OK","The entered record matches the existing data in the database. No change has been made.",emp.model_dump(mode="json"))
        
        update_one = await employeeCollection.update_one(
            {"employeeID": id},
            {"$set": employeeDict}
        )
        if update_one.acknowledged:
            return successHTTP("OK",f"Employee Information Updated with the ID: {id}",emp.model_dump(mode="json"))
        else:
            clientErrorHandling(200,"OK","An Error has been occured on updating information",emp.model_dump(mode="json"))
    except Exception as e:
        raise serverErrorHandling(e)
    
async def softDeleteEmployee(id:str,isActive:bool):
    try:
        employeeCheck = await employeeCollection.find_one({"employeeID":id},{})
        print(employeeCheck)
        if employeeCheck is None:
            raise clientErrorHandling(404,"OK",f"Employee ID not Found: {id}",{"isActive":isActive})
        elif isActive == employeeCheck["isActive"]:
            raise clientErrorHandling(200,"OK","The data entered is the same. No change has been made.",{"isActive":isActive})
        else:
            softDeleteEmployee = await employeeCollection.update_one(
                {"employeeID": id},
                {"$set": {"isActive":isActive}}
            )
            if softDeleteEmployee.acknowledged:
                print(softDeleteEmployee.acknowledged)
                return successHTTP("OK",f"Employee Information Updated(Soft Deleted) ID: {id}")
            else:
                clientErrorHandling(200,"OK","An Error has been occured on updating information")
    except Exception as e:
        raise serverErrorHandling(e)