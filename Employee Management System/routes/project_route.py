from fastapi import APIRouter,HTTPException
from Controller.projectManagementController import  createProject,updateProject
from Controller.taskManagementController import createTask,updateTask
from Models.models import ProjectModel,TaskModel

router = APIRouter()


@router.post("/createProject")
async def add_project(project: ProjectModel):
    projectResult = await createProject(project)
    return projectResult

@router.put("/updateProject")
async def update_Project(id:str,project: ProjectModel):
    projectResult = await updateProject(id,project)
    return projectResult

@router.post("/createTask")
async def add_Task(task:TaskModel):
    projectResult= await createTask(task)
    return projectResult

@router.patch("/updateTask")
async def update_Task(taskID:str,task:TaskModel):
    taskResult= await updateTask(taskID,task)
    return taskResult