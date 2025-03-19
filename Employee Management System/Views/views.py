from datetime import datetime
from itertools import zip_longest

assigned_employees = []


def employee_viewer(employees):
    output= f"Available Employees\n\n"
    for employee in employees:
        if employee["isActive"]==True: 
            output+= f"Employee ID: {employee["employeeID"]}\n"
            output+= f"Name: {employee['firstName']} {employee['lastName']}\n\n"
    return output.strip()



def projectTask_viewer(projects, tasks, employee):
    output= ""
    for project in projects:
        output+= f"{project["projectName"]}\n"
        for task in tasks:
            
            if project["projectID"] == task["projectID"]:
                output += f"Task\n"
                output += f"ID: {task["taskID"]}\n"
                output += f"Name: {task["taskName"]}\n"
                output += f"Description: {task["taskDescription"]}\n"
                output += f"Status: {task["taskStatus"]}\n"
                if task["assignEmployee"] == "None":
                    output += f"Assigned To: None\n\n"
                else:
                    output += f"Assigned To: "
                    for e in employee:
                        if e["employeeID"] in task["assignEmployee"]:
                           output += f"{e['firstName']} {e['lastName']}, " 
                    output = output.rstrip(", ")   
                    output += "\n\n"
        output+= f"==================================================================\n"
    return output.strip()


def project_viewer(projects,employees,tasks):
    output="Ongoing Projects\n\n"
        
    for project in projects:
        progress = progressProject(tasks,project["projectID"])
        if progress != "Completed":
            output += displayProject(project,employees,tasks)
    return output

def projectHistory_viewer(projects,employees,tasks):
    output="Project History\n"
        
    for project in projects:
        progress = progressProject(tasks,project["projectID"])
        if progress != "Not yet started":
            output += displayProject(project,employees,tasks)
    return output

def displayProject(projects,employees,tasks):
    output = ""
    output += f"{projects.get('projectName', 'Unnamed Project')}\n"
    output += f"Description: {projects.get('projectDescription', 'No Description')}\n"
    output += f"Target Date: {projects['projectTargetDate'].strftime('%B %d, %Y')}\n"
    output += f"Start Date: {projects['projectStartDate'].strftime('%B %d, %Y')}\n"
    output += f"Assigned Employee:"
    output += f" {assignedEmployee(employees,tasks,projects["projectID"])}\n"
    output += f"Progress: {progressProject(tasks,projects["projectID"])}\n\n"
    output += f"\n"
    return output

def assignedEmployee(employee,task,projectID):
    output=""
    employeeSet = set()
    for t in task:
        if t["projectID"] == projectID and t["assignEmployee"] != "None":
            for e in employee:
                if e["employeeID"] in t["assignEmployee"] and e["employeeID"] not in employeeSet:
                    employeeSet.add(e["employeeID"])
                    output += f"({e['firstName']} {e['lastName']}),"
                
    output = output.rstrip(", ")   
    if output == "":
        output = "None"
    return output

def progressProject(tasks,projectID):
    taskCount = 0
    taskDone = 0
    for task in tasks:
        if task["projectID"] == projectID:
            taskCount += 1

        if task["projectID"] == projectID and task["taskStatus"] == "Done":
            taskDone +=1
    progress = round((taskDone/taskCount)*100) if taskCount and taskDone else 0
    if progress == 0:
        return "Not yet started"
    elif progress == 100:
        return "Completed"
    else:
        return f"{progress}%"
