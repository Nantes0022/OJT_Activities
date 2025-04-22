from fastapi import APIRouter,Header
from Controller.employee_controllers import all_employees,employee_by_id, employee_by_status, employee_by_department,employee_by_position
from Controller.projectManagementController import  getAllProject,getProjectHistory
from Controller.taskManagementController import getProjectTask
from Views.views import view_employee, project_viewer, projectTask_viewer,projectHistory_viewer
from fastapi.responses import PlainTextResponse
from datetime import datetime
from ErrorHandling.errorHandling import credentials_exception

router = APIRouter()


#Employee View Collection
@router.get("/api/v1/employees/{employeeId}")
async def list_employee_by_Id(employeeId:str):
    print("By ID")
    employees = await employee_by_id(employeeId)
    return view_employee(employees)

@router.get("/api/v1/employees")
async def list_employee(isActive: bool=None,department: str = None,position:str = None):
    if isActive is not None:
        print("status")
        employees = await employee_by_status(isActive)
        return view_employee(employees)
    elif department is not None:
        print("department")
        employees = await employee_by_department(department)
        return view_employee(employees)
    elif position is not None:   
        print("By status")
        employees = await employee_by_position(position)
        return view_employee(employees)
    else:
        print("All")
        employees = await all_employees()
        return view_employee(employees)

#Project view collection
@router.get("/api/v1/projects")
async def list_Project():
    projects, employees, tasks = await getAllProject()
    return project_viewer(projects,employees,tasks)


@router.get("/api/v1/projects/history")
async def list_Project_History():
    projects, employees, tasks = await getProjectHistory()
    return projectHistory_viewer(projects,employees,tasks)


#Task view collection
@router.get("/api/v1/task")
async def list_Project_Task():
    projects, tasks, employee = await getProjectTask()
    return projectTask_viewer(projects,tasks,employee)
