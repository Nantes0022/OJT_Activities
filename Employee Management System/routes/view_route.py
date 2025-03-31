from fastapi import APIRouter
from Controller.projectManagementController import  getAllEmployee,getAllProject,getProjectHistory
from Controller.taskManagementController import getProjectTask
from Views.views import employee_viewer, project_viewer, projectTask_viewer,projectHistory_viewer
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/getAvailableEmployee")
async def list_employee():
    employees = await getAllEmployee()
    return employee_viewer(employees)

@router.get("/getOngoingProjects")
async def list_Project():
    projects, employees, tasks = await getAllProject()
    return project_viewer(projects,employees,tasks)

@router.get("/getProjectTask")
async def list_Project_Task():
    projects, tasks, employee = await getProjectTask()
    return projectTask_viewer(projects,tasks,employee)

@router.get("/projectHistory")
async def list_Project_History():
    projects, employees, tasks = await getProjectHistory()
    return projectHistory_viewer(projects,employees,tasks)