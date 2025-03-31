from connection.database import db
from Models.models import TaskModel
from ErrorHandling.errorHandling import clientErrorHandling,serverErrorHandling,successHTTP
from fastapi import HTTPException
from traceback import format_exc

employeeCollection = db["employeeList"]
projectCollection = db["projectList"]
taskCollection = db["taskList"]

async def createTask(task:TaskModel):
    try:
        tasks = task.model_dump()
        req_Fields = ['projectID','taskName']
        miss_Fields = [field for field in req_Fields if not tasks.get(field)]  
        checkProject = await projectCollection.find_one({"projectID": tasks["projectID"]})
        taskCount = await taskCollection.count_documents({})
        tasks["taskID"] = str(taskCount + 1)
        emp_req = [emp_req] if isinstance(emp_req := tasks["assignEmployee"], str) else emp_req
        employee,resultID = await checkEmployee(tasks["assignEmployee"])
        if miss_Fields:
            raise clientErrorHandling(400, "Bad Request", f"Missing required fields: {', '.join(miss_Fields)}",task.model_dump(mode="json"))
        elif not checkProject:
            raise clientErrorHandling(404, "Not Found", "Project ID not Found",task.model_dump(mode="json"))
        elif employee:
            raise clientErrorHandling(404, "Not Found", f"Employee not Found: {', '.join(resultID)}",task.model_dump(mode="json"))
        
        
        newTask = await taskCollection.insert_one(tasks)
        if newTask.acknowledged:
            return successHTTP("OK",f"Task Created to {tasks['projectID']}",task.model_dump())
        else:
            raise clientErrorHandling(500,"Internal Server Error","An Error has been occured on updating information",task.model_dump(mode="json"))
    except Exception as e:
        raise serverErrorHandling(e)
    

    
async def checkEmployee(assignEmployee):
    employeeAssign = assignEmployee
    employeeCheck=False
    employeeID = []
    for aE in employeeAssign:
        print(f"Processing Employee ID: {aE}")
        
        employee = await employeeCollection.find_one({"employeeID": aE})  # No need for empty projection {}

        if not employee:
            employeeCheck = True
            employeeID.append(str(aE))
    return employeeCheck,employeeID
    
async def updateTask(taskID:str,task:TaskModel):
    try:
        tasks = task.model_dump(exclude_unset=True)
        cursor = employeeCollection.find()
        checkTask = await taskCollection.find_one({"taskID": taskID})
        employee = await cursor.to_list(length=None)   
        employee_ids = {e["employeeID"] for e in employee}

        checkEmployee = False
        for ae in tasks["assignEmployee"]:
            if ae not in employee_ids:
                checkEmployee = True
                break

        if checkEmployee == False and checkTask:
            updateTask = await taskCollection.update_one(
                {"taskID": taskID},
                {"$set": tasks} 
            )
            if (updateTask.acknowledged):
                return clientErrorHandling(201,f"Task Information Updated: {taskID}")
        else:
            return clientErrorHandling(201,"Task ID or EmployeeID Not Found.")
    except Exception as e:
        raise serverErrorHandling(e)
    
    

    
    
    
async def getProjectTask():
    try:
        projects = await projectCollection.find().to_list()
        tasks = await taskCollection.find().to_list()
        employee = await employeeCollection.find().to_list()
        return projects, tasks, employee
    except Exception as e:
        raise serverErrorHandling(e)