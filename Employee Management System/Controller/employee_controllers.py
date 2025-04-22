from connection.database import db
from Models.models import Employee
from ErrorHandling.errorHandling import clientErrorHandling,serverErrorHandling,successHTTP
from fastapi import HTTPException
import json
from traceback import format_exc

employeeCollection = db['employeeList']

async def createEmployee(emp: Employee):
    try:
        print("TRY BLOCK EXECUTING")  # Debugging log
        employeeDict = emp.model_dump()
        req_Fields = ['employeeId','firstName','lastName','email']
        miss_Fields = [field for field in req_Fields if not employeeDict.get(field)]
        employeeCheck = await employeeCollection.find_one({"employeeId": employeeDict["employeeId"]})

        if miss_Fields:
            raise clientErrorHandling(400, "Bad Request", f"Missing required fields: {', '.join(miss_Fields)}",emp.model_dump(mode="json"))  
        elif employeeCheck:
            raise clientErrorHandling(409, "Conflict", f"Employee ID {employeeDict['employeeId']} already exists.",emp.model_dump(mode="json"))
            
        employee = await employeeCollection.insert_one(employeeDict)
        if employee.acknowledged:
            print("EMPLOYEE INSERTED SUCCESSFULLY")  
            return successHTTP( "Created", f"Employee Information Inserted",emp.model_dump(mode="json"))
        else:
            clientErrorHandling(200,"OK","An Error has been occured on updating information",emp.model_dump(mode="json"))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)

        
    
async def updateEmployee(employeeId:str,emp: Employee):
    try:
        employeeDict = emp.model_dump(exclude_unset=True)
        if not employeeDict:
            print("EMPTY RESPONSE BODY")  
            raise clientErrorHandling(200,"OK","Response Body is empty",emp.model_dump(mode="json"))
        
        update_one = await employeeCollection.update_one(
            {"employeeId": employeeId},
            {"$set": employeeDict}
        )

        if update_one.modified_count == 0:
            raise clientErrorHandling(200,"OK","The entered record matches the existing data in the database. No change has been made.",emp.model_dump(mode="json"))
        elif update_one.acknowledged:
            return successHTTP("OK",f"Employee Information Updated with the ID: {employeeId}",emp.model_dump(mode="json"))
        else:
            clientErrorHandling(200,"OK","An Error has been occured on updating information",emp.model_dump(mode="json"))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)
    
async def softDeleteEmployee(employeeId:str,isActive:bool):
    try:
        employeeCheck = await employeeCollection.find_one({"employeeId":employeeId},{})
        if employeeCheck is None:
            raise clientErrorHandling(404,"OK",f"Employee ID not Found: {employeeId}",{"isActive":isActive})
        else:
            softDeleteEmployee = await employeeCollection.update_one(
                {"employeeId": employeeId},
                {"$set": {"isActive":isActive}}
            )
            if softDeleteEmployee.modified_count == 0:
                raise clientErrorHandling(200,"OK","The data entered is the same. No change has been made.",{"isActive":isActive})
            else:
                return successHTTP("OK",f"Employee Information Updated(Soft Deleted) ID: {employeeId}",{"isActive":isActive})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)
    
async def all_employees():
    try:
        employees = await employeeCollection.find({},{"_id":0,"employeeId": 1, "firstName": 1, "lastName": 1,"isActive":1}).to_list()
        return employees
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)
    
async def employee_by_id(employeeId:str):
    try:
        employees = await employeeCollection.find_one({"employeeId":employeeId},{"_id":0,"employeeId": 1, "firstName": 1, "lastName": 1})
        return employees
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)
    
async def employee_by_status(isActive:bool):
    try:
        employees = await employeeCollection.find(
            {"isActive": isActive}, 
            {"_id": 0, "employeeId": 1, "firstName": 1, "lastName": 1, "isActive": 1} 
        ).to_list()
        return employees
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)

async def employee_by_department(department:str):
    try:
        employees = await employeeCollection.find(
            {"department": department}, 
            {"_id": 0, "employeeId": 1, "firstName": 1, "lastName": 1, "isActive": 1}  
        ).to_list()
        return employees
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)

async def employee_by_position(position:str):
    try:
        employees = await employeeCollection.find(
            {"position": position}, 
            {"_id": 0, "employeeId": 1, "firstName": 1, "lastName": 1, "isActive": 1}  
        ).to_list()
        return employees
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)            