from connection.database import db
from Models.models import Task
from ErrorHandling.errorHandling import clientErrorHandling,serverErrorHandling,successHTTP
from fastapi import HTTPException
from traceback import format_exc

employeeCollection = db["employeeList"]
projectCollection = db["projectList"]
taskCollection = db["taskList"]

async def createTask(task:Task):
    try:
        tasks = task.model_dump()
        req_Fields = ['taskId','projectId','name']
        miss_Fields = [field for field in req_Fields if not tasks.get(field)]  
        checkProject = await projectCollection.find_one({"projectId": tasks["projectId"]})
        taskCheck = await taskCollection.find_one({"taskId":tasks["taskId"]})
        emp_req = [emp_req] if isinstance(emp_req := tasks["assignEmployee"], str) else emp_req
        employee,resultID = await checkEmployee(tasks["assignEmployee"])
        if miss_Fields:
            raise clientErrorHandling(400, "Bad Request", f"Missing required fields: {', '.join(miss_Fields)}",task.model_dump(mode="json"))
        elif not checkProject:
            raise clientErrorHandling(404, "Not Found", "Project ID not Found",task.model_dump(mode="json"))
        elif employee:
            raise clientErrorHandling(404, "Not Found", f"Employee not Found: {', '.join(resultID)}",task.model_dump(mode="json"))
        elif not tasks["taskId"]:
            raise clientErrorHandling(404, "Not Found",f"Task ID is empty",task.model_dump(mode="json",exclude_unset=True))
        elif taskCheck:
            raise clientErrorHandling(409,"Conflict",f"Task ID {tasks["taskId"]} Already Exist",task.model_dump(mode="json",exclude_unset=True))
        
        newTask = await taskCollection.insert_one(tasks)
        if newTask.acknowledged:
            return successHTTP("OK",f"Task Created to {tasks['projectId']}",task.model_dump())
        else:
            raise clientErrorHandling(500,"Internal Server Error","An Error has been occured on updating information",task.model_dump(mode="json"))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)
    

    
async def checkEmployee(assignEmployee):
    employeeAssign = assignEmployee
    employeeCheck=False
    employeeID = []
    for aE in employeeAssign:
        print(f"Processing Employee ID: {aE}")
        
        employee = await employeeCollection.find_one({"employeeId": aE})  # No need for empty projection {}

        if not employee:
            employeeCheck = True
            employeeID.append(str(aE))
    return employeeCheck,employeeID
    
async def updateTask(taskID:str,task:Task):
    try:
        
        tasks = task.model_dump(exclude_unset=True)
        cursor = employeeCollection.find()
        checkTask = await taskCollection.find_one({"taskId": taskID})
        employee = await cursor.to_list(length=None)   
        employee_ids = {e["employeeId"] for e in employee}
        req_Fields = ['projectId','name','status']
        miss_Fields = [field for field in req_Fields if not tasks.get(field)]

        
        if miss_Fields:
            raise clientErrorHandling(422, "error", f"Missing required fields: {', '.join(miss_Fields)}",task.model_dump(mode="json",exclude_unset=True)) 
        else:
            checkEmployee = False
            for ae in tasks["assignEmployee"]:
                if ae not in employee_ids:
                    checkEmployee = True
                    break
            if checkEmployee == True:
                raise clientErrorHandling(404, "Not Found", f"Employee not Found",task.model_dump(mode="json"))
                
            updateTask = await taskCollection.update_one(
                {"taskId": taskID},
                {"$set": tasks} 
            )
            if (updateTask.modified_count == 0):
                raise clientErrorHandling(200,"Not Modified","The entered record matches the existing data in the database. No change has been made.",task.model_dump(mode="json",exclude_unset=True))
            else:
                return successHTTP("OK",f"Task updated to {tasks['projectId']}",task.model_dump())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)
    
    

    
    
    
async def getProjectTask():
    try:
        projects = await projectCollection.find().to_list()
        tasks = await taskCollection.find().to_list()
        employee = await employeeCollection.find().to_list()
        return projects, tasks, employee
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)