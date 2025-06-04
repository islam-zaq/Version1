from models.employee import Employee
from models.position import Position
from models.document import Document
from models.salary import Salary
from models.car import Car
from models.cash import Cash
from models.credit_card import CreditCard
from utils.helpers import display_table
from utils.menuEmployee import *
import sqlite3
from datetime import datetime
class Menu:
    def __init__(self):
        self.employee = Employee()
        self.position = Position()
        self.document = Document()
        self.salary = Salary()
        self.car = Car()
        self.credit_card = CreditCard()
        self.cash = Cash()

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Manage Employees")
            print("2. Manage Positions")
            print("3. Manage Salaries")
            print("4. Manage Cars")
            print("5. Manage Credit Cards")
            print("6. Manage Cash")
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.employee_menu()
            elif choice == "2":
                self.position_menu()
            elif choice == "3":
                self.salary_menu()
            elif choice == "4":
                self.car_menu()
            elif choice == "5":
                self.credit_card_menu()
            elif choice == "6":
                self.cash_document_menu()
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
            print("8. Export to csv file")
            print("9. Import from csv file")
            print("0. Back")
            choice = input("Enter your choice: ")

            if   choice == "1":
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
            elif choice == "5": # View fired employees
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
            elif choice == "7": # Unfire an employee
                employees = self.employee.read_fired_employees()
                display_table(employees, ["ID", "Name", "Position"], "Fired Employees")
                emp_id = input("Enter employee ID to restore: ")
                self.employee.unfire_employee(emp_id)
            elif choice == "8": # Export to csv
                filename = input("Enter filename: ").strip()
                self.employee.export_employees_to_csv(filename)
            elif choice == "9": # Import from csv
                filename = input("Enter filename: ").strip()
                self.employee.import_employees_from_csv(filename)
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
            print("8. Export to csv file")
            print("9. Import from csv file")
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
            elif choice == "8": # Export to csv
                filename = input("Enter filename: ").strip()
                self.position.export_positions_to_csv(filename)
            elif choice == "9": # Import from csv
                filename = input("Enter filename: ").strip()
                self.position.import_positions_from_csv(filename)
            elif choice == "0":
                break
            else:
                print("Invalid choice, try again.")

    def salary_menu(self):
        while True:
            print("\nSalary Menu:")
            print("1. Add Salary Record")
            print("2. View Salaries")
            print("3. Update Salary")
            print("4. Delete Salary")
            print("5. Export to csv file")
            print("6. Import from csv file")
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
            elif choice == "5": # Export to csv
                filename = input("Enter filename: ").strip()
                self.salary.export_salaries_to_csv(filename)
            elif choice == "6": # Import from csv
                filename = input("Enter filename: ").strip()
                self.salary.import_salaries_from_csv(filename)            
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
            print("5. Export to csv file")
            print("6. Import from csv file")    
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
            elif choice == "5":
                filename = input("Enter filename: ").strip()
                self.car.export_cars_to_csv(filename)
            elif choice == "6":
                filename = input("Enter filename: ").strip()
                self.car.import_cars_from_csv(filename)
            elif choice == "0":
                break
            else:
                print("Invalid choice, try again.")

    def to_int(self, value):
        try:
            return int(value)
        except:
            return 0

    def to_float(self, value):
        try:
            return float(value)
        except:
            return 0

    def credit_card_menu(self):
        while True:
            print("\nCredit card Menu:")
            print("1. Add Credit card")
            print("2. View Credit cards")
            print("3. Update Credit card")
            print("4. Delete Credit card")
            print("5. Export to csv file")
            print("6. Import from csv file")
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
            elif choice == "5":
                filename = input("Enter filename: ").strip()
                self.credit_card.export_credit_cards_to_csv(filename)
            elif choice == "6":
                filename = input("Enter filename: ").strip()
                self.credit_card.import_credit_cards_from_csv(filename)
            elif choice == "0":
                break
            else:
                print("Invalid choice, try again.")
    
    def cash_menu(self, doc_id):
        while True:
            print("1. Add money")
            print("2. Add sub money")
            print("3. Update money")
            print("4. Delete money")
            print("5. Show deleted money")
            print("6. Filter settings")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "1":
                m100 = m50 = m20 = m10 = m5 = m1 = 0
                tenne = 0
                d100 = d50 = d20 = d10 = d5 = d2 = d1 = 0
                rate = summa = 0
                sumCom = ""
                comment = ""
                date    = datetime.now()

                while True:
                    print("\n--- CASH MENU ---")
                    print("1. 100m:      ", m100, " = ", self.to_int(m100) * 100)
                    print("2. 50m:       ", m50,  " = ", self.to_int(m50) * 50)
                    print("3. 20m:       ", m20,  " = ", self.to_int(m20) * 20)
                    print("4. 10m:       ", m10,  " = ", self.to_int(m10) * 10)
                    print("5. 5m:        ", m5,   " = ", self.to_int(m5) * 5)
                    print("6. 1m:        ", m1)
                    print("7. Tenne:     ", tenne)

                    print("8. 100$:      ", d100, " = ", self.to_int(d100) * 100 * self.to_float(rate))
                    print("9. 50$:       ", d50,  " = ", self.to_int(d50) * 50   * self.to_float(rate))
                    print("10. 20$:      ", d20,  " = ", self.to_int(d20) * 20   * self.to_float(rate))
                    print("11. 10$:      ", d10,  " = ", self.to_int(d10) * 10   * self.to_float(rate))
                    print("12. 5$:       ", d5,   " = ", self.to_int(d5) * 5     * self.to_float(rate))
                    print("13. 2$:       ", d2,   " = ", self.to_int(d2) * 2     * self.to_float(rate))
                    print("14. 1$:       ", d1)

                    print("15. Rate:     ", rate)
                    print("16. Summa:    ", summa)
                    print("17. Sum comm: ", sumCom)
                    print("18. Comment:  ", comment)
                    print("19. Date:     ", date)
                    print("0. Exit")                    
                    
                    choice = input("Enter your choice: ")
                                    
                    if choice == "1":
                        m100 = self.to_int(input("100m: "))
                    elif choice == "2":
                        m50 = self.to_int(input("50m: "))
                    elif choice == "3":
                        m20 = self.to_int(input("20m: "))
                    elif choice == "4":
                        m10 = self.to_int(input("10m: "))
                    elif choice == "5":
                        m5 = self.to_int(input("5m: "))
                    elif choice == "6":
                        m1 = self.to_int(input("1m: "))
                    elif choice == "7":
                        tenne = self.to_int(input("Tenne: "))
                    elif choice == "8":
                        d100 = self.to_int(input("100$: "))
                    elif choice == "9":
                        d50 = self.to_int(input("50$: "))
                    elif choice == "10":
                        d20 = self.to_int(input("20$: "))
                    elif choice == "11":
                        d10 = self.to_int(input("10$: "))
                    elif choice == "12":
                        d5 = self.to_int(input("5$: "))
                    elif choice == "13":
                        d2 = self.to_int(input("2$: "))
                    elif choice == "14":
                        d1 = self.to_int(input("1$: "))
                    elif choice == "15":
                        rate = self.to_float(input("Rate: "))
                    elif choice == "16":
                        summa = self.to_float(input("Summa: "))
                    elif choice == "17":
                        sumCom = self.to_float(input("Sum comm: "))
                    elif choice == "18":
                        comment = input("Comment: ")
                    elif choice == "19":
                        date = input("Date: ")
                    elif choice == "0":
                        print("Exiting...")
                        break
                    else:
                        print("Invalid choice, try again.")
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice, try again.")

    def cash_document_menu(self):
        while True:
            cash_documents = self.cash.read_cash_documents()
            display_table(cash_documents, ["ID", "Doc date", "Comment", "Status"], "Cash documents")

            print("Cash Documents Menu:")
            print("1. Enter")
            print("2. Create Cash Document")
            print("3. Delete Cash Document")
            print("4. Activate Cash Document")
            print("0. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                cash_documents = self.cash.read_cash_documents()
                display_table(cash_documents, ["ID", "Doc date", "Comment", "Status"], "Cash documents")

                doc_id = input("Enter document ID to use: ")                
                doc_info = next((doc for doc in cash_documents if str(doc[0]) == doc_id), None)
                if doc_info:
                    self.cash_menu(doc_id)
                else:
                    print("Invalid id.")


            elif choice == "2":
                sene = input("Enter date (format:2025-12-31): ")
                comment = input("Enter title: ")
                self.cash.create_cash_document(sene, comment)
            elif choice == "3":
                cash_documents = self.cash.read_cash_documents()
                display_table(cash_documents, ["ID", "Doc date", "Comment", "Status"], "Cash documents")
                
                doc_id = input("Enter document ID to delete: ")                
                doc_info = next((doc for doc in cash_documents if str(doc[0]) == doc_id), None)
                if doc_info and self.confirm_deletion_fire("Cash document", doc_info[1], doc_id):
                    self.cash.delete_document(doc_id)
                else:
                    print("Deletion canceled.")
            elif choice == "4":
                cash_documents = self.cash.read_cash_documents(True)
                display_table(cash_documents, ["ID", "Doc date", "Comment", "Status"], "Cash documents")

                doc_id = input("Enter document ID to delete: ")                
                doc_info = next((doc for doc in cash_documents if str(doc[0]) == doc_id), None)
                if doc_info:
                    self.cash.activate_document(doc_id)
                else:
                    print("Activation canceled.")
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice, try again.")