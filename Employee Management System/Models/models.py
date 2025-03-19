from pydantic import BaseModel,field_validator
from typing import Optional,List
from datetime import datetime

class EmployeeCreateModel(BaseModel):
    employeeID: str
    firstName: str
    lastName: str
    email: str
    position: str
    department: str
    dateJoined: datetime
    isActive:bool

class EmployeeUpdateModel(BaseModel):
    employeeID: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    dateJoined: Optional[str] = None
    isActive:bool

class ProjectCreateModel(BaseModel):
    projectID:str
    projectName:str
    projectDescription:str
    projectTargetDate:datetime
    projectStartDate:datetime

class ProjectUpdateModel(BaseModel):
    projectName:Optional[str] = None
    projectDescription:Optional[str] = None
    projectTargetDate:Optional[datetime] = None
    projectStartDate:Optional[datetime] = None


class TaskModel(BaseModel):
    taskID:Optional[str] = None
    projectID:Optional[str] = None
    taskName:Optional[str] = None
    taskDescription:Optional[str] = None
    taskStatus:Optional[str] = None
    assignEmployee:Optional[List] = None
