from datetime import datetime
from itertools import zip_longest
from ErrorHandling.errorHandling import serverErrorHandling
from traceback import format_exc

assigned_employees = []


def employee_viewer(employees):
    try:
        data = {
        "available employee": [
            {"employeeID": emp["employeeID"], "firstName": emp["firstName"], "lastName": emp["lastName"]}
            for emp in employees if emp["isActive"]
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
            data["activeTask"][task["taskID"]] = {
                "taskName": task["taskName"], 
                "taskDescription": task["taskDescription"],
                "projectID": project["projectID"],
                "taskStatus":task["taskStatus"],
                "assignedEmployee": [
                        {"firstName": emp["firstName"], "lastName": emp["lastName"]}
                        for emp in employee if emp["employeeID"] in task.get("assignEmployee", [])  # Avoids KeyError
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
            statusData=progressProject(project["projectID"],tasks)
            if statusData != condition:
                datas[goto][project["projectID"]] = {
                    "projectName": project["projectName"], 
                    "projectDescription": project["projectDescription"],
                    "projectTargetDate": datetime.fromisoformat(str(project["projectTargetDate"])).strftime("%Y-%m-%d"),
                    "projectStartDate":datetime.fromisoformat(str(project["projectStartDate"])).strftime("%Y-%m-%d"),
                    "progress": statusData,
                    "assignedEmployee": [
                            {"firstName": first, "lastName": last}
                                for first, last in {
                                    (emp["firstName"], emp["lastName"])
                                    for task in tasks if task["projectID"] == project["projectID"]
                                    for emp in employees if emp["employeeID"] in task.get("assignEmployee", [])
                            }]
                }
        return datas
    except Exception as e:
        raise serverErrorHandling(e)

def progressProject(projID,tasks):
    taskCount = 0
    taskDone = 0
    for task in tasks:
        if projID == task["projectID"]:
           taskCount += 1

        if projID == task["projectID"] and task["taskStatus"] == "Done":
            taskDone +=1
    progress = round((taskDone/taskCount)*100) if taskCount and taskDone else 0
    if progress == 0:
        return "Not yet started"
    elif progress == 100:
        return "Completed"
    else:
        return f"{progress}%"
