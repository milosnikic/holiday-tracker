from tinydb import TinyDB

from db import DBBroker
from models import Category, Employee


class Controller:
    def __init__(self) -> None:
        self.db_broker = DBBroker(TinyDB("db.json"))

    def get_all_employees(self):
        return self.db_broker.get_all(Employee)

    def add_new_employee(self, employee: Employee):
        id = self.db_broker.add(employee, Employee)
        employee.id = id
        return employee

    def update_employee(self, employee: Employee):
        return self.db_broker.update(
            employee,
            employee.id,
            Employee,
        )

    def get_employee_by_id(self, id: int):
        return self.db_broker.get(id, Employee)

    def add_new_category(self, category: str):
        return self.db_broker.add(Category(category), Category)

    def get_all_categories(self):
        return self.db_broker.get_all(Category)
