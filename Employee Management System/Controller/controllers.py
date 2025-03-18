from connection.database import db
from Models.models import EmployeeModel

employeeCollection = db['employeeList']

async def createEmployee(emp: EmployeeModel):
    employeeDict = emp.model_dump()
    newUser = await employeeCollection.insert_one(employeeDict)
    if (newUser.acknowledged):
        return str(employeeDict["employeeID"])
    else:
        return "null"
    
async def updateEmployee(id,emp: EmployeeModel):
    employeeDict = emp.model_dump(exclude_unset=True)
    updateUser = await employeeCollection.update_one(
        {"employeeID": id},
        {"$set": employeeDict}
    )
    if (updateUser.acknowledged):
        return str(id)
    else:
        return "null"
    
async def softDeleteEmployee(id,emp: EmployeeModel):
    employeeDict = emp.model_dump(exclude_unset=True)
    softDeleteEmployee = await employeeCollection.update_one(
        {"employeeID": id},
        {"$set": employeeDict}
    )
    if (softDeleteEmployee.acknowledged):
        return str(id)
    else:
        return "null"
