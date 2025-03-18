from pydantic import BaseModel,field_validator
from typing import Optional,List
from datetime import datetime

class EmployeeModel(BaseModel):
    employeeID: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    dateJoined: Optional[str] = None
    isActive:bool

class ProjectModel(BaseModel):
    projectID:Optional[str] = None
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
