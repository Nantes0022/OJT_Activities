from connection.database import db
from Models.models import TaskModel

employeeCollection = db["employeeList"]
projectCollection = db["projectList"]
taskCollection = db["taskList"]

async def createTask(task:TaskModel):
    tasks = task.model_dump()
    cursor = employeeCollection.find()
    checkProject = await projectCollection.find_one({"projectID": tasks["projectID"]})
    employee = await cursor.to_list(length=None)   
    employee_ids = {e["employeeID"] for e in employee}

    checkEmployee = False
    for ae in tasks["assignEmployee"]:
        if ae not in employee_ids:
            checkEmployee = True
            break
    if checkEmployee == False:
        newTask = await taskCollection.insert_one(tasks)
        return f"The task has been created with ProjectID {tasks['projectID']}"

    return "No Project ID or EmployeeID Found."

    
async def updateTask(taskID:str,task:TaskModel):
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
            return taskID
        else:
            return "null"
    return "Task ID or EmployeeID Not Found."
    

    
   
    
    
async def getProjectTask():
    projects = await projectCollection.find().to_list()
    tasks = await taskCollection.find().to_list()
    employee = await employeeCollection.find().to_list()
    return projects, tasks, employee