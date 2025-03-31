from fastapi import APIRouter
from Controller.controllers import createEmployee,updateEmployee,softDeleteEmployee
from Models.models import EmployeeModel

router = APIRouter()

@router.post("/createEmployee")
async def add_employee(emp: EmployeeModel):
    employeeResult = await createEmployee(emp)
    return employeeResult

@router.put("/updateEmployee")
async def update_employee(id:str,emp: EmployeeModel):
    employeeResult = await updateEmployee(id, emp)
    return employeeResult

@router.patch("/deleteEmployee")
async def patch_employee(id:str,isActive:bool):
    employeeResult = await softDeleteEmployee(id, isActive)
    return employeeResult
