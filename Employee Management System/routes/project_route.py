from fastapi import APIRouter,HTTPException
from Controller.projectManagementController import  createProject,assignEmployeeToProj,getAllEmployee,getAllProject
from Controller.taskManagementController import createTask,updateTask,getProjectTask
from Models.models import ProjectModel,TaskModel
from Views.views import employee_viewer, project_viewer, projectTask_viewer
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.post("/createProject")
async def add_project(project: ProjectModel):
    projectResult = await createProject(project)
    return f"The project with ProjectID {projectResult} has been created."

@router.put("/assignEmployeeProject")
async def assign_employee_to_proj(employeeID:str,projectID:str):
    employeeResult = await assignEmployeeToProj(employeeID,projectID)
    return f"{employeeResult}"

@router.post("/createTask")
async def add_Task(task:TaskModel):
    projectResult= await createTask(task)
    return f"{projectResult}"

@router.patch("/updateTask")
async def update_Task(taskID:str,task:TaskModel):
    taskResult= await updateTask(taskID,task)
    return f"The task has been update with taskID {taskResult}"