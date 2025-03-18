from fastapi import FastAPI
from routes.employee_route import router as employee_route
from routes.project_route import router as project_route
from routes.view_route import router as view_route

app = FastAPI()

app.include_router(employee_route)
app.include_router(project_route)
app.include_router(view_route)


@app.get("/")
def home():
    return "Welcome to Employee Management!"