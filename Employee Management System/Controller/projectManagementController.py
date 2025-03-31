from connection.database import db
from Models.models import ProjectModel
from ErrorHandling.errorHandling import clientErrorHandling,serverErrorHandling,successHTTP
from traceback import format_exc
from fastapi import HTTPException

projectCollection = db["projectList"]
employeeCollection = db["employeeList"]
taskCollection = db["taskList"]

async def createProject(project: ProjectModel):
    try:
        proj = project.model_dump()
        projectCheck = await projectCollection.find_one({"projectID":proj["projectIDs"]})
        req_Fields = ['projectID','projectName','projectStartDate']
        miss_Fields = [field for field in req_Fields if not proj.get(field)]
        print(miss_Fields)
        if miss_Fields:
            raise clientErrorHandling(422, "error", f"Missing required fields: {', '.join(miss_Fields)}",project.model_dump(mode="json",exclude_unset=True)) 
        elif projectCheck:
            print("PROJECT ID ALREADY EXIST")  
            raise clientErrorHandling(409,"Conflict",f"Project ID {proj["projectID"]} Already Exist",project.model_dump(mode="json",exclude_unset=True))
        
        newProject = await (projectCollection.insert_one(proj))
        if newProject.acknowledged:
            return successHTTP("Created",f"Project Information Inserted",project.model_dump(mode="json",exclude_unset=True))
        else:
            raise clientErrorHandling(200,"OK","An Error has been occured on updating information",project.model_dump(mode="json",exclude_unset=True))
    except Exception as e:
        raise serverErrorHandling(e)
    
    
async def updateProject(id:str,project: ProjectModel):
    try:
        projectDict = project.model_dump(exclude_unset=True)
        projectCheck = await projectCollection.find_one({"projectID":id},{})
        
        if projectCheck is None:
            raise clientErrorHandling(404,"Not Found","Project ID not Found",project.model_dump(mode="json",exclude_unset=True))
        elif not projectDict:
            print("EMPTY RESPONSE BODY")  
            raise clientErrorHandling(200,"OK","Response Body is empty",project.model_dump(mode="json",exclude_unset=True))
        elif all(projectDict.get(key) == projectCheck.get(key) for key in projectDict):
            print("RECORD ARE THE SAME")  
            raise clientErrorHandling(200,"Not Modified","The entered record matches the existing data in the database. No change has been made.",project.model_dump(mode="json",exclude_unset=True))
        update_Result = await projectCollection.update_one(
                {"projectID": id},
                {"$set": projectDict}
            )
        if update_Result.acknowledged:
            return successHTTP("OK",f"Project Information Updated. ID: {id}",project.model_dump(mode="json",exclude_unset=True))
        else:
            raise clientErrorHandling(500,"Internal Server Error","An Error has been occured on updating information",project.model_dump(mode="json"))
    except Exception as e:
        raise serverErrorHandling(e)
async def getAllEmployee():
    try:
        employees = await employeeCollection.find().to_list()
        return employees
    except Exception as e:
        raise serverErrorHandling(e)
      
async def getAllProject():
    try:
        employees = await employeeCollection.find().to_list()
        projects = await projectCollection.find().to_list()
        tasks = await taskCollection.find().to_list()
        return projects,employees,tasks
    except Exception as e:
        raise serverErrorHandling(e)

async def getProjectHistory():
    try:
        employees = await employeeCollection.find().to_list()
        projects = await projectCollection.find().to_list()
        tasks = await taskCollection.find().to_list()
        return projects,employees,tasks
    except Exception as e:
        raise serverErrorHandling(e)
