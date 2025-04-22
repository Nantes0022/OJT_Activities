from datetime import datetime
from itertools import zip_longest
from ErrorHandling.errorHandling import serverErrorHandling
from traceback import format_exc

assigned_employees = []


def view_employee(employees):
    try:
        data = {
        "available employee": [
            employees
            ]
        }    
        return data
    except Exception as e:
        raise serverErrorHandling(e)


def projectTask_viewer(projects, tasks, employee):
    try:
        data = {
        "activeTasks": {}
        }
        for task,project in zip(tasks,projects):
            data["activeTasks"][task["taskId"]] = {
                "name": task["name"], 
                "description": task["taskDescription"],
                "projectId": project["projectId"],
                "taskStatus":task["taskStatus"],
                "assignedEmployee": [
                        {"firstName": emp["firstName"], "lastName": emp["lastName"]}
                        for emp in employee if emp["employeeID"] in task.get("assignEmployee", [])
                    ]
            }
        
        return data
    except Exception as e:
        raise serverErrorHandling(e)
        
    


def project_viewer(projects,employees,tasks):
    try:
        data = {
            "ongoingProject": {}
        }

        return projectData(projects,tasks,employees,data,"ongoingProject","Completed")
    except Exception as e:
        raise serverErrorHandling(e)

def projectHistory_viewer(projects,employees,tasks):
    try:
        data = {
            "projectHistory": {}
        }

        return projectData(projects,tasks,employees,data,"projectHistory","Not yet started")
    except Exception as e:
        raise serverErrorHandling(e)

def projectData(projects,tasks,employees,data,goto,condition):
    try:
        datas = data
        for project in projects:
            statusData=progressProject(project["projectId"],tasks)
            startDateString=""
            TargetDateString=""
            if project["startDate"] != None:
                startDateString=datetime.fromisoformat(str(project["startDate"])).strftime("%Y-%m-%d")
            
            if project["targetDate"] != None:
                TargetDateString=datetime.fromisoformat(str(project["targetDate"])).strftime("%Y-%m-%d")
            if statusData != condition:
                datas[goto][project["projectId"]] = {
                    "name": project["name"], 
                    "description": project["description"],
                    "targetDate": startDateString,
                    "startDate":TargetDateString,
                    "progress": statusData,
                    "assignedEmployee": [
                            {"firstName": first, "lastName": last}
                                for first, last in {
                                    (emp["firstName"], emp["lastName"])
                                    for task in tasks if task["projectId"] == project["projectId"]
                                    for emp in employees if emp["employeeId"] in task.get("assignEmployee", [])
                            }]
                }
        return datas
    except Exception as e:
        raise serverErrorHandling(e)

def progressProject(projID,tasks):
    taskCount = 0
    taskDone = 0
    for task in tasks:
        if projID == task["projectId"]:
           taskCount += 1

        if projID == task["projectId"] and task["status"] == "Done":
            taskDone +=1
    progress = round((taskDone/taskCount)*100) if taskCount and taskDone else 0
    if progress == 0:
        return "Not yet started"
    elif progress == 100:
        return "Completed"
    else:
        return f"{progress}%"
