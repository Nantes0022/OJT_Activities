from connection.database import db
from Models.models import ProjectCreateModel,ProjectUpdateModel
from Views.views import employee_viewer

projectCollection = db["projectList"]
employeeCollection = db["employeeList"]
taskCollection = db["taskList"]

async def createProject(project: ProjectCreateModel):
    proj = project.model_dump()
    projectCheck = await projectCollection.find_one({"projectID":proj["projectID"]})
    if projectCheck:
        return "Project ID Already Exist"
    elif proj["projectID"] == "":
        return "Please fill up Project ID"
    else:
        newProject = await (projectCollection.insert_one(proj))
        return f"The project with ProjectID {proj["projectID"]} has been created."
    
async def updateProject(id:str,project: ProjectUpdateModel):
    projectDict = project.model_dump(exclude_unset=True)
    projectCheck = await projectCollection.find_one({"projectID":id})
    if projectCheck is None:
        return "Employee ID not Found"
    else:
        await projectCollection.update_one(
            {"projectID": id},
            {"$set": projectDict}
        )
        return f"The employee with EmployeeID {id} has been updated."
    
async def getAllEmployee():
    return await employeeCollection.find().to_list()
      
async def getAllProject():
    employees = await employeeCollection.find().to_list()

    projects = await projectCollection.find().to_list()

    tasks = await taskCollection.find().to_list()

    return projects,employees,tasks

async def getProjectHistory():
    employees = await employeeCollection.find().to_list()

    projects = await projectCollection.find().to_list()

    tasks = await taskCollection.find().to_list()

    return projects,employees,tasks
