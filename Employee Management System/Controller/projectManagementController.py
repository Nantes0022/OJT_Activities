from connection.database import db
from Models.models import ProjectModel
from Views.views import employee_viewer

projectCollection = db["projectList"]
employeeCollection = db["employeeList"]
taskCollection = db["taskList"]

async def createProject(project: ProjectModel):
    proj = project.model_dump()
    newProject = await (projectCollection.insert_one(proj))
    if (newProject.acknowledged):
        return str(proj["projectID"])
    else:
        return "null"
    
async def getAllEmployee():
    return await employeeCollection.find({},{"_id":0,"employeeID":1,"firstName": 1,"lastName":1}).to_list()
    
async def assignEmployeeToProj(employeeID:str,projectID:str): 

    employees = await employeeCollection.find_one({"employeeID":employeeID})
    projects = await projectCollection.find_one({"projectID":projectID}, {"_id": 0, "projectID": 1,"assignedEmployee": 1})
    if employees is None and projects is None:
        return "No Employee ID and Project ID found"
    elif employees is None:
        return "No Employee ID found"
    elif projects is None:
        return "No Project ID found"
    else:
        if(projects["assignedEmployee"]=="None"):
            updateProject = await projectCollection.update_one(
                {"projectID": projectID},
                {"$set": {"assignedEmployee":[employeeID]}}
            )
            if (updateProject.acknowledged):
                return f"The project with ProjectID {str(projectID)} has been updated"
        else:
            updateProject = await projectCollection.update_one(
                {"projectID": projectID},
                {"$addToSet": {"assignedEmployee":employeeID}}
            )
            if updateProject.modified_count > 0:
                return f"The project with ProjectID {projectID} has been assigned to EmployeeID {employeeID}."
            else:
                return f"No changes were made, EmployeeID {employeeID} has been already assigned to ProjectID {projectID}."
            
async def getAllProject():
    employees = await employeeCollection.find(
        {}, {"_id": 0, "employeeID": 1, "firstName": 1, "lastName": 1}
    ).to_list()

    projects = await projectCollection.find(
        {}, {
            "_id": 0, 
            "projectID": 1,
            "projectName": 1,
            "projectDescription": 1,
            "projectTargetDate": 1,
            "projectStartDate": 1,
            "assignedEmployee": 1,
            "progress": 1
        }
    ).to_list()

    tasks = await taskCollection.find().to_list()

    return projects,employees,tasks
