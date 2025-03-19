from connection.database import db
from Models.models import EmployeeCreateModel, EmployeeUpdateModel

employeeCollection = db['employeeList']

async def createEmployee(emp: EmployeeCreateModel):
    employeeDict = emp.model_dump()
    employeeCheck = await employeeCollection.find_one({"employeeID":employeeDict["employeeID"]})
    if employeeCheck:
        return "Employee ID Already Exist"
    elif employeeDict["employeeID"] == "":
        return "Please fill up Project ID"
    else:
        await employeeCollection.insert_one(employeeDict)
        return f"The employee with EmployeeID {employeeDict["employeeID"]} has been created."
    
async def updateEmployee(id:str,emp: EmployeeUpdateModel):
    employeeDict = emp.model_dump(exclude_unset=True)
    employeeCheck = await employeeCollection.find_one({"employeeID":id})
    if employeeCheck is None:
        return "Employee ID not Found"
    else:
        updateUser = await employeeCollection.update_one(
            {"employeeID": id},
            {"$set": employeeDict}
        )
        return f"The employee with EmployeeID {id} has been updated."
    
async def softDeleteEmployee(id:str,isActive:bool):
    employeeCheck = await employeeCollection.find_one({"employeeID":id})
    if employeeCheck is None:
        return "Employee ID not Found"
    else:
        softDeleteEmployee = await employeeCollection.update_one(
            {"employeeID": id},
            {"$set": {"isActive":isActive}}
        )
        return f"The Status of Employee ID {id} has been updated."
