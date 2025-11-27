# empleados.py - Sistema de Registro y Control de Empleados 
# API para la gestión de empleados de TechNova, que permite registrar, consultar, actualizar y eliminar empleados del sistema.
# fastapi dev Exercises/exercise_02/empleados.py

from fastapi import FastAPI, HTTPException
from base_model import *

app = FastAPI(openapi_tags= ['Employees Register'])

@app.get('/employees')
async def list_view():
    return employees_list

@app.get('/emplyees/{id}', status_code= 200)
async def employee_view(id: int):
    for employee in employees_list:
        if employee.id == id:
            return employee
    raise HTTPException(status_code= 404, detail={'Error': 'Empleado no registrado'})

@app.post('/employees', status_code= 201)
async def employee_register(new_employee: Employees):
    for employee in employees_list:
        if new_employee.id == employee.id:
            raise HTTPException(status_code= 409, detail={'Error': 'Empleado ya existente'})
    employees_list.append(new_employee)
    return new_employee

@app.put('/employees', status_code= 200)
async def employee_update(employee: Employees):
    found= False
    for index, saved_employee in enumerate(employees_list):
        if saved_employee.id == employee.id:
            employees_list[index] = employee
            found= True
            break
    if not found:
        raise HTTPException(status_code=404, detail={'Error': 'Empleado no actualizado'})
    return employee

@app.delete('/employees/{id}', status_code= 200)
async def employee_delete(id: int):
    for employee in employees_list:
        if employee.id == id:
            employees_list.remove(employee)
            return {'Message': 'Empleado eleiminado con exito'}
    raise HTTPException(status_code= 404, detail= {'Error': 'Empleado no existente'})
