from fastapi import APIRouter,Header,Depends,HTTPException,Request
from Controller.employee_controllers import createEmployee,updateEmployee,softDeleteEmployee
from Models.models import Employee
from Controller.user_controller import check_if_admin_role
from ErrorHandling.errorHandling import credentials_exception,serverErrorHandling

router = APIRouter()




@router.post("/api/v1/employees")
async def add_employee(emp: Employee,request:Request):
    try:
        Authorization = request.headers.get("Authorization")
        token = Authorization[7:]
        is_admin = check_if_admin_role(token)
        print(is_admin)
        if not is_admin:
            print("if condition")
            raise credentials_exception() 
            
        employeeResult = await createEmployee(emp)
        return employeeResult
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)


@router.patch("/api/v1/employees/{employeeId}")
async def update_employee(employeeId:str,emp: Employee,request:Request): 
    try:  
        Authorization = request.headers.get("Authorization")
        token = Authorization[7:]
        is_admin = check_if_admin_role(token)
        print(is_admin)
        if not is_admin:
            print("if condition")
            raise credentials_exception() 
        employeeResult = await updateEmployee(employeeId, emp)
        return employeeResult
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)

@router.patch("/api/v1/employees/{employeeId}/{isActive}")

async def patch_employee(employeeId:str,isActive:bool,request:Request): 
    try:  
        Authorization = request.headers.get("Authorization")
        token = Authorization[7:]
        is_admin = check_if_admin_role(token)
        print(is_admin)
        if not is_admin:
            print("if condition")
            raise credentials_exception()  
        employeeResult = await softDeleteEmployee(employeeId, isActive)
        return employeeResult
    except HTTPException as e:
        raise e
    except Exception as e:
        raise serverErrorHandling(e)
