from fastapi import APIRouter,HTTPException
from Controller.controllers import createEmployee,updateEmployee,softDeleteEmployee
from Models.models import EmployeeCreateModel,EmployeeUpdateModel

router = APIRouter()

@router.post("/createEmployee")
async def add_employee(emp: EmployeeCreateModel):
    employeeResult = await createEmployee(emp)
    return employeeResult

@router.put("/updateEmployee")
async def update_employee(id:str,emp: EmployeeUpdateModel):
    employeeResult = await updateEmployee(id, emp)
    return employeeResult

@router.patch("/deleteEmployee")
async def patch_employee(id:str,isActive:bool):
    employeeResult = await softDeleteEmployee(id, isActive)
    return employeeResult
