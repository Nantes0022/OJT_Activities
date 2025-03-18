from fastapi import APIRouter,HTTPException
from Controller.controllers import createEmployee,updateEmployee,softDeleteEmployee
from Models.models import EmployeeModel

router = APIRouter()

@router.post("/createEmployee")
async def add_employee(emp: EmployeeModel):
    employee_id = await createEmployee(emp)
    return f"The employee with EmployeeID {employee_id} has been created."

@router.put("/updateEmployee")
async def update_employee(id:int,emp: EmployeeModel):
    employee_id = await updateEmployee(id, emp)
    return f"The employee with EmployeeID {employee_id} has been updated."

@router.patch("/deleteEmployee")
async def patch_employee(id:int,emp: EmployeeModel):
    employee_id = await softDeleteEmployee(id, emp)
    return str(emp.employeeID)
