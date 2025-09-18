from models.employee import Employee
from models.position import Position
from models.document import Document
from models.salary import Salary
from models.car import Car
from models.credit_card import CreditCard
from utils.helpers import display_table
import sqlite3

class Menu:
    def __init__(self):
        self.employee = Employee()
        self.position = Position()
        self.document = Document()
        self.salary = Salary()
        self.car = Car()
        self.credit_card = CreditCard()

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Manage Employees")
            print("2. Manage Positions")
            # print("3. Manage Documents")
            print("3. Manage Salaries")
            print("4. Manage Cars")
            print("5. Manage Credit Cards")
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.employee_menu()
            elif choice == "2":
                self.position_menu()
            # elif choice == "3":
            #     self.document_menu()
            elif choice == "3":
                self.salary_menu()
            elif choice == "4":
                self.car_menu()
            elif choice == "7":
                self.credit_card_menu()
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice, try again.")

    def confirm_deletion_fire(self, item_type, item_name, item_id):
        confirm = input(
            f"Are you sure you want to delete/fire {item_type} '{item_name}' (ID: {item_id})? (yes/y/1): ")
        return confirm.lower() in ["yes", "y", "1"]

    def employee_menu(self):
        while True:
            print("\nEmployee Menu:")
            print("1. Add Employee")
            print("2. View Employees")
            print("3. Update Employee")
            print("4. Delete Employee")
            print("5. View fired Employees")
            print("6. Fire Employee")
            print("7. Unfire Employee")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter employee name: ")
                
                positions = self.position.read_positions()
                display_table(positions, ["ID", "Title"], "Positions")
                position_id = input("Enter position ID: ")
                
                self.employee.create_employee(name, position_id)
                
            elif choice == "2":
                employees = self.employee.read_employees()
                display_table(employees, ["ID", "Name", "Position"], "Employees")
                
            elif choice == "3":
                employees = self.employee.read_employees()
                display_table(employees, ["ID", "Name", "Position"], "Employees")
                emp_id = input("Enter employee ID to update: ")
                existing_employee = next((emp for emp in employees if str(emp[0]) == emp_id), None)
                if not existing_employee:
                    print("Invalid employee ID.")
                    continue

                name = input("Enter new name (leave blank to keep current): ") or existing_employee[1]
                positions = self.position.read_positions()
                display_table(positions, ["ID", "Title"], "Positions")
                existing_position = next((pos for pos in positions if str(pos[1]) == existing_employee[2]), None)
                if not existing_position:
                    print("Invalid position ID.")
                    continue
                position_id = input("Enter new position ID (leave blank to keep current): ") or existing_position[0]

                self.employee.update_employee(emp_id, name, position_id)
                
            elif choice == "4":
                employees = self.employee.read_employees()
                display_table(employees, ["ID", "Name", "Position"], "Employees")

                emp_id = input("Enter employee ID to delete: ")
                emp_info = next((emp for emp in employees if str(emp[0]) == emp_id), None)
                if emp_info and self.confirm_deletion_fire("employee", emp_info[1], emp_id):
                    self.employee.delete_employee(emp_id)
                else:
                    print("Deletion canceled.")
            elif choice == "5":  # View fired employees
                employees = self.employee.read_fired_employees()
                display_table(employees, ["ID", "Name", "Position"], "Fired Employees")
            elif choice == "6": #Fire Employee
                employees = self.employee.read_employees()
                display_table(employees, ["ID", "Name", "Position"], "Employees")
                emp_id = input("Enter employee ID to fire: ")
                emp_info = next((emp for emp in employees if str(emp[0]) == emp_id), None)
                if emp_info and self.confirm_deletion_fire("employee", emp_info[1], emp_id):
                    self.employee.fire_employee(emp_id)
                else:
                    print("Deletion canceled.")
            elif choice == "7":  # Unfire an employee
                employees = self.employee.read_fired_employees()
                display_table(employees, ["ID", "Name", "Position"], "Fired Employees")
                emp_id = input("Enter employee ID to restore: ")
                self.employee.unfire_employee(emp_id)
            elif choice == "0":
                break
            else:
                print("Invalid choice, try again.")

    def position_menu(self):
        while True:
            print("\nPosition Menu:")
            print("1. Add Position")
            print("2. View Positions")
            print("3. Update Position")
            print("4. Delete Position")
            print("5. View Inactive Position")
            print("6. Deactivate Position")
            print("7. Reactivate Position")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "1":
                title = input("Enter position title: ")
                existing_positions = [pos[1].lower() for pos in self.position.read_positions()]
                if title.lower() in existing_positions:
                    print("❌ Error: This position already exists.")
                else:
                    self.position.create_position(title)
                   
            elif choice == "2":
                positions = self.position.read_positions()
                display_table(positions, ["ID", "Title"], "Positions")
                
            elif choice == "3":
                positions = self.position.read_positions()
                display_table(positions, ["ID", "Title"], "Positions")
                pos_id = input("Enter position ID to update: ")
                existing_position = next((pos for pos in positions if str(pos[0]) == pos_id), None)
                if not existing_position:
                    print("Invalid position ID.")
                    continue

                new_title = input("Enter new title (leave blank to keep current): ") or existing_position[1]

                self.position.update_position(pos_id, new_title)
                
            elif choice == "4":
                positions = self.position.read_positions()
                display_table(positions, ["ID", "Title"], "Positions")
                pos_id = input("Enter position ID to delete: ")
                pos_info = next((pos for pos in positions if str(pos[0]) == pos_id), None)
                if pos_info and self.confirm_deletion_fire("position", pos_info[1], pos_id):
                    self.position.delete_position(pos_id)
                else:
                    print("Deletion canceled.")
            elif choice == "5":  # View Inactive Positions
                positions = self.position.read_inactive_positions()
                display_table(positions, ["ID", "Title"], "Inactive Positions")
            elif choice == "6":  # Deactivate Position
                positions = self.position.read_positions()
                display_table(positions, ["ID", "Title"], "Active Positions")
                pos_id = input("Enter position ID to deactivate: ")
                self.position.deactivate_position(pos_id)
            elif choice == "7":  # Reactivate Position
                positions = self.position.read_inactive_positions()
                display_table(positions, ["ID", "Title"], "Inactive Positions")
                pos_id = input("Enter position ID to reactivate: ")
                self.position.reactivate_position(pos_id)
            elif choice == "0":
                break
            else:
                print("Invalid choice, try again.")
    # def document_menu(self):
    #     while True:
    #         print("\nDocument Menu:")
    #         print("1. Add Document")
    #         print("2. View Documents")
    #         print("3. Update Document")
    #         print("4. Delete Document")
    #         print("0. Back")
    #         choice = input("Enter your choice: ")
    #
    #         if choice == "1":
    #             title = input("Enter document title: ")
    #             description = input("Enter description: ")
    #             date = input("Enter date (YYYY-MM-DD): ")
    #             worked_date = input("Enter worked days: ")
    #             self.document.create_document(title, description, date, worked_date)
    #         elif choice == "2":
    #             documents = self.document.read_documents()
    #             display_table(documents, ["ID", "Title", "Description", "Date", "Worked Days"], "Documents")
    #         elif choice == "3":
    #             documents = self.document.read_documents()
    #             display_table(documents, ["ID", "Title", "Description", "Date", "Worked Days"], "Documents")
    #             doc_id = input("Enter document ID to update: ")
    #             existing_document = next((doc for doc in documents if str(doc[0]) == doc_id), None)
    #             if not existing_document:
    #                 print("Invalid document ID.")
    #                 continue
    #
    #             title = input("Enter new title (leave blank to keep current): ") or existing_document[1]
    #             description = input("Enter new description (leave blank to keep current): ") or existing_document[2]
    #             date = input("Enter new date (YYYY-MM-DD, leave blank to keep current): ") or existing_document[3]
    #             worked_date = input("Enter new worked days (leave blank to keep current): ") or existing_document[4]
    #
    #             self.document.update_document(doc_id, title, description, date, worked_date)
    #         elif choice == "4":
    #             documents = self.document.read_documents()
    #             display_table(documents, ["ID", "Title", "Description", "Date", "Worked Days"], "Documents")
    #             doc_id = input("Enter document ID to delete: ")
    #             doc_info = next((doc for doc in documents if str(doc[0]) == doc_id), None)
    #             if doc_info and self.confirm_deletion_fire("document", doc_info[1], doc_id):
    #                 self.document.delete_document(doc_id)
    #             else:
    #                 print("Deletion canceled.")
    #         elif choice == "0":
    #             break
    #         else:
    #             print("Invalid choice, try again.")
    #
    def salary_menu(self):
        while True:
            print("\nSalary Menu:")
            print("1. Add Salary Record")
            print("2. View Salaries")
            print("3. Update Salary")
            print("4. Delete Salary")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "1":
                amount = input("Enter amount: ")

                employees = self.employee.read_employees()
                display_table(employees, ["ID", "Name", "Position"], "Employees")

                employeeId = input("Enter employee id: ")

                self.salary.create_salary(amount, employeeId)
            elif choice == "2":
                salaries = self.salary.read_salaries()
                display_table(salaries, ["ID", "Emp.id", "Employee", "Amount", "Position"], "Salaries")
                self.salary.sum_salary()
            elif choice == "3":
                salaries = self.salary.read_salaries()
                display_table(salaries, ["ID", "Emp.id", "Amount", "Employee"], "Salaries")
                sal_id = input("Enter salary ID to update: ")
                existing_salary = next((sal for sal in salaries if str(sal[0]) == sal_id), None)
                if not existing_salary:
                    print("Invalid salary ID.")
                    continue

                amount = input("Enter new amount (leave blank to keep current): ") or existing_salary[2]

                employees = self.employee.read_employees()
                display_table(employees, ["ID", "Name", "Position"], "Employees")
                employee_id = input("Enter new employee ID (leave blank to keep current): ") or existing_salary[1]

                self.salary.update_salary(sal_id, amount, employee_id)
            elif choice == "4":
                salaries = self.salary.read_salaries()
                display_table(salaries, ["ID", "Emp.id", "Amount", "Employee"], "Salaries")
                sal_id = input("Enter salary ID to delete: ")
                sal_info = next((sal for sal in salaries if str(sal[0]) == sal_id), None)
                if sal_info and self.confirm_deletion_fire("salary record", sal_info[2], sal_id):
                    self.salary.delete_salary(sal_id)
                else:
                    print("Deletion canceled.")
            elif choice == "0":
                break
            else:
                print("Invalid choice, try again.")

    def car_menu(self):
        while True:
            print("\nCar Menu:")
            print("1. Add Car")
            print("2. View Cars")
            print("3. Update Car")
            print("4. Delete Car")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "1":
                model = input("Enter car model: ")
                car_idnum = input("Enter car ID number: ")

                employees = self.employee.read_employees()
                display_table(employees, ["ID", "Name", "Position"], "Employees")

                owner1_id = input("Enter primary owner ID: ")
                owner2_id = input("Enter secondary owner ID (optional): ") or None

                try:
                    self.car.create_car(model, car_idnum, owner1_id, owner2_id)
                except sqlite3.IntegrityError as e:
                    print(f"❌ Error adding car: {e}")
            elif choice == "2":
                cars = self.car.read_cars()
                display_table(cars, ["ID", "Model", "Car ID", "Owner 1", "Owner 2"], "Cars")

            elif choice == "3":
                cars = self.car.read_cars()
                display_table(cars, ["ID", "Model", "Car ID", "Owner 1", "Owner 2"], "Cars")
                car_id = input("Enter car ID to update: ")
                existing_car = next((car for car in cars if str(car[0]) == car_id), None)
                if not existing_car:
                    print("Invalid car ID.")
                    continue

                model = input("Enter new model (leave blank to keep current): ") or existing_car[1]
                car_idnum = input("Enter new car ID number (leave blank to keep current): ") or existing_car[2]

                employees = self.employee.read_employees()
                display_table(employees, ["ID", "Name", "Position"], "Employees")

                existing_employee1 = next((emp for emp in employees if str(emp[1]) == existing_car[3]), None)
                existing_employee2 = next((emp1 for emp1 in employees if str(emp1[1]) == existing_car[4]), None)

                if not existing_employee1:
                    print("Invalid employee ID.")
                    continue

                if not existing_employee2:
                    print("Invalid employee ID.")
                    continue

                employee_id1 = input("Enter new primary owner ID (leave blank to keep current): ") or existing_employee1[0]
                employee_id2 = input("Enter new secondary owner ID (leave blank to keep current): ") or existing_employee2[0]
                print(employee_id2)
                self.car.update_car(car_id, model, car_idnum, employee_id1, employee_id2)

            elif choice == "4":
                cars = self.car.read_cars()
                display_table(cars, ["ID", "Model", "Car ID", "Owner 1", "Owner 2"], "Cars")
                car_id = input("Enter car ID to delete: ")
                car_info = next((car for car in cars if str(car[0]) == car_id), None)
                if car_info and self.confirm_deletion_fire("car", car_info[1], car_id):
                    self.car.delete_car(car_id)
                else:
                    print("Deletion canceled.")
            elif choice == "0":
                break
            else:
                print("Invalid choice, try again.")

    def credit_card_menu(self):
        while True:
            print("\nCredit card Menu:")
            print("1. Add Credit card")
            print("2. View Credit cards")
            print("3. Update Credit card")
            print("4. Delete Credit card")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == '1':
                amount = input("Enter amount: ")

                employees = self.employee.read_employees()
                display_table(employees, ["ID", "Name", "Position"], "Employees")

                employeeId = input("Enter employee id: ")

                self.credit_card.create_credit_card(amount,employeeId)
            elif choice == '2':
                credit_card = self.credit_card.read_credit_cards()
                display_table(credit_card, ["ID", "Emp. ID", "Name", "title", "Amount", "Gecyani", "Pensiya", "Tutum",
                                            "Edara"], "Credit card")
                self.credit_card.sum_credit_card()
            elif choice == '3':
                credit_card = self.credit_card.read_credit_cards()
                display_table(credit_card, ["ID", "Emp. ID", "Name", "title", "Amount", "Gecyani", "Pensiya", "Tutum",
                                            "Edara"], "Credit card")
                self.credit_card.sum_credit_card()

                card_id = input("Enter the ID of the credit card record to update: ")

                existing_card = next((card for card in credit_card if str(card[0]) == card_id), None)
                if not existing_card:
                    print("Invalid card ID.")
                    continue

                amount = input("Enter new credit card amount (leave blank to keep current): ") or existing_card[4]

                employees = self.employee.read_employees()
                display_table(employees, ["ID", "Name", "Position"], "Employees")

                print("Choose a new employee for this credit card (leave blank to keep current):")
                employee_id = input("Enter employee ID (leave blank to keep current): ") or existing_card[1]

                self.credit_card.update_credit_card(card_id, amount, employee_id)

            elif choice == '4':
                credit_card = self.credit_card.read_credit_cards()
                display_table(credit_card,
                              ["ID", "Emp. ID", "Name", "title", "Amount", "Gecyani", "Pensiya", "Tutum", "Edara"],
                              "Credit card")
                self.credit_card.sum_credit_card()

                card_id = input("Enter the ID of the credit card record to delete: ")

                card_info = next((card for card in credit_card if str(card[0]) == card_id), None)
                if card_info and self.confirm_deletion_fire("card", card_info[1], card_id):
                    self.credit_card.delete_credit_card(card_id)
                else:
                    print("Deletion canceled.")

            elif choice == "0":
                break
            else:
                print("Invalid choice, try again.")