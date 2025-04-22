from pydantic import BaseModel,field_validator
from typing import Optional,List,Union
from datetime import datetime


class Employee(BaseModel):
    employeeId: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    dateJoined: Optional[datetime] = None
    isActive:Optional[bool] = None


class Project(BaseModel):
    projectId:Optional[str] = None
    name:Optional[str] = None
    description:Optional[str] = None
    targetDate:Optional[datetime] = None
    startDate:Optional[datetime] = None


class Task(BaseModel):
    taskId:Optional[str] = None
    projectId:Optional[str] = None
    name:Optional[str] = None
    description:Optional[str] = None
    status:Optional[str] = None
    assignEmployee:Optional[Union[List[str], str]] = None

class User(BaseModel):
    userId:Optional[str] = None
    username:Optional[str] = None
    password:Optional[str] = None
    email:Optional[str] = None
    mobilenumber:Optional[str] = None
    role:Optional[str] = None

class AuthToken(BaseModel):
    token: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None
    createdAt: Optional[datetime] = None
    expiresAt: Optional[datetime] = None
    isActive: Optional[bool]=None
