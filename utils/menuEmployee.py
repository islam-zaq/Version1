def menuEmployee(self):
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