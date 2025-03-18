from datetime import datetime

assigned_employees = []


def employee_viewer(employees):
    output= f"Available Employees\n\n"
    for employee in employees:
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
    output = "Ongoing Projects\n\n"
    taskProject = [t["assignEmployee"] for t in tasks]
    for project in projects:
        task_count = sum(1 for task in tasks if project["projectID"] == task["projectID"])
        task_completed_count = sum(1 for task in tasks if task["taskStatus"] == "Done" and project["projectID"] == task["projectID"])
        
        progress = 0

        progress = round((task_completed_count/task_count)*100)
        if progress == 0:
            output += f"{project.get('projectName', 'Unnamed Project')}\n"
            output += f"Description: {project.get('projectDescription', 'No Description')}\n"
            output += f"Target Date: {project['projectTargetDate'].strftime('%B %d, %Y')}\n"
            output += f"Start Date: {project['projectStartDate'].strftime('%B %d, %Y')}\n"
            output += f"Assigned Employee:\n"
            output += f"Progress: Not started yet\n\n"
        elif progress != 100:
            output += f"{project.get('projectName', 'Unnamed Project')}\n"
            output += f"Description: {project.get('projectDescription', 'No Description')}\n"
            output += f"Target Date: {project['projectTargetDate'].strftime('%B %d, %Y')}\n"
            output += f"Start Date: {project['projectStartDate'].strftime('%B %d, %Y')}\n"
            output += f"Assigned Employee:\n"
            output += f"Progress: {round((task_completed_count/task_count)*100)}%\n\n"
    return output.strip()

#Process ng pagpapadisplay ng ongoing projects
def outputDisplay(project,employees,tasks):
    
    output = ""
    
    for task in tasks:
        print(task)

    output += "\n"
    return output