from fastapi import APIRouter,Header,HTTPException,Request
from Controller.projectManagementController import  createProject,updateProject
from Controller.taskManagementController import createTask,updateTask
from Models.models import Project,Task
from Controller.user_controller import check_if_admin_role
from ErrorHandling.errorHandling import credentials_exception, serverErrorHandling

router = APIRouter()


@router.post("/api/v1/projects")
async def add_project(project: Project,request:Request):
    try:  
        Authorization = request.headers.get("Authorization")
        token = Authorization[7:]
        is_admin = check_if_admin_role(token)
        print(is_admin)
        if not is_admin:
            print("if condition")
            raise credentials_exception() 
        projectResult = await createProject(project)
        return projectResult
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)
    
@router.patch("/api/v1/projects/{projectId}")
async def update_Project(projectId:str,project: Project,request:Request):
    try:  
        Authorization = request.headers.get("Authorization")
        token = Authorization[7:]
        is_admin = check_if_admin_role(token)
        print(is_admin)
        if not is_admin:
            print("if condition")
            raise credentials_exception() 
        projectResult = await updateProject(projectId,project)
        return projectResult
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)
    
@router.post("/api/v1/task")
async def add_Task(task:Task,request:Request):
    try:  
        Authorization = request.headers.get("Authorization")
        token = Authorization[7:]
        is_admin = check_if_admin_role(token)
        print(is_admin)
        if not is_admin:
            print("if condition")
            raise credentials_exception() 
        projectResult= await createTask(task)
        return projectResult
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)

@router.patch("/api/v1/task/{taskId}")
async def update_Task(taskId:str,task:Task,request:Request):
    try:  
        Authorization = request.headers.get("Authorization")
        token = Authorization[7:]
        is_admin = check_if_admin_role(token)
        print(is_admin)
        if not is_admin:
            print("if condition")
            raise credentials_exception() 
        taskResult= await updateTask(taskId,task)
        return taskResult
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)