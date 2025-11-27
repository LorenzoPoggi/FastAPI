# base_model.py - Sistema de Registro y Control de Empleados 
# Base de Datos simulada

from pydantic import BaseModel

class Employees (BaseModel):
    id: int
    name: str
    position: str
    salary: float
    active: bool

employees_list = []