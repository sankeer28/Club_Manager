from datetime import datetime

class User:
    def __init__(self, username, password, role, email, phone, name=None, address=None, payment_preferences=None, payment_status="Unpaid", attendance_count=0, notification_preferences=None, payment_history=None):
        self.username = username
        self.password = password
        self.role = role
        self.email = email
        self.phone = phone
        self.name = name
        self.address = address
        self.payment_preferences = payment_preferences
        self.payment_status = payment_status
        self.attendance_count = attendance_count
        self.notification_preferences = notification_preferences if notification_preferences else {}
        self.payment_history = payment_history if payment_history else []

    def add_payment(self, amount, date):
        self.payment_history.append({"amount": amount, "date": date})

    def receive_notification(self, message):
        print("Received notification:", message)

class Club:
    SESSION_FEE = 10  # Fee for each practice session

    def __init__(self):
        self.users = []  # Store user data (username, password, role, email, phone)
        self.attendance = {}  # Store member attendance (username: count)
        self.payments = {}  # Store member payments (username: amount paid)
        self.unpaid_debt = {}  # Store unpaid debt (username: amount owed)
        self.coaches = []  # Store coach details (name, contact info, etc.)
        self.practice_schedule = {}  # Store practice details (date, time, location)
        self.expenses = {}  # Store monthly expenses (month: total expenses)
        self.monthly_payables = {}  # Store current month's account payables (username: amount)

    def load_users_from_file(self):
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    fields = line.strip().split(',')
                    if len(fields) == 9:
                        username, password, role, email, phone, payment_status, attendance_count, notification_preferences, payment_history = fields
                        user = User(username, password, role, email, phone, payment_status, int(attendance_count), eval(notification_preferences), eval(payment_history))
                        self.users.append(user)
                        # Check if the user is a coach and add them to the coach list
                        if role == 'Coach':
                            self.coaches.append({'name': username, 'contact_info': email})  # Assuming email as contact info
                    elif len(fields) == 5:  # If line represents practice schedule
                        date, time, location, coach = fields
                        self.practice_schedule[date] = {"time": time, "location": location, "coach": coach}
                    else:
                        print("Invalid data format in the file.")
        except FileNotFoundError:
            print("No existing user data found.")

    def save_users_to_file(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                payment_history_str = str(user.payment_history).replace("'", "\"")  # Convert to string and replace single quotes with double quotes
                file.write(f"{user.username},{user.password},{user.role},{user.email},{user.phone},{user.payment_status},{user.attendance_count},{user.notification_preferences},{payment_history_str}\n")
            for date, details in self.practice_schedule.items():
                file.write(f"{date},{details['time']},{details['location']},{details['coach']}\n")

    def register_member(self):
        print("Please enter the following details to register:")
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Enter role (Member/Coach/Treasurer): ")
        email = input("Enter email: ")
        phone = input("Enter phone: ")
        name = input("Enter name: ")
        address = input("Enter address: ")
        payment_preferences = input("Enter payment preferences: ")
        new_member = User(username, password, role, email, phone, name, address, payment_preferences)
        self.users.append(new_member)
        self.save_users_to_file()  # Save user information to file
        print("New member registered successfully.")

    def manage_coach_list(self, treasurer):
        if treasurer.role == "Treasurer":
            print("Coach List:")
            with open('users.txt', 'r') as file:
                for line in file:
                    fields = line.strip().split(',')
                    if len(fields) == 9 and fields[2] == 'Coach':
                        print(f"Name: {fields[0]}")
            print("\n1. Add Coach")
            print("2. Back")
            option = input("Enter your choice (1-2): ")
            if option == "1":
                coach_name = input("Enter coach's name: ")
                contact_info = input("Enter coach's contact info: ")
                coach_details = {"name": coach_name, "contact_info": contact_info}
                self.coaches.append(coach_details)
                print("Coach added successfully.")
            elif option == "2":
                print("Returning to main menu...")
            else:
                print("Invalid choice.")
        else:
            print("Only the treasurer can manage the coach list.")

    def manage_schedule(self, treasurer):
        if treasurer.role == "Treasurer":
            print("Scheduled Practices:")
            for date, details in self.practice_schedule.items():
                print(f"Date: {date}, Time: {details['time']}, Location: {details['location']}, Coach: {details['coach']}")
            print("\n1. Back")
            option = input("Enter your choice (1): ")
            if option == "1":
                print("Returning to main menu...")
            else:
                print("Invalid choice.")
        else:
            print("Only the treasurer can manage the schedule.")

    def schedule_practice(self, coach):
        if coach.role == "Coach":
            date = input("Enter practice date (YYYY-MM-DD): ")
            time = input("Enter practice time: ")
            location = input("Enter practice location: ")
            practice_details = {"date": date, "time": time, "location": location, "coach": coach.username}
            self.practice_schedule[date] = practice_details
            self.save_users_to_file()  # Save schedule to file
            print("Practice scheduled successfully.")
            for user in self.users:
                if user.role == "Member":
                    print(f"Reminder: Practice scheduled on {date} at {time} in {location}.")
        else:
            print("Only the coach can schedule practices.")

    def members_schedule_and_pay_for_practice(self, member):
        if member.role == "Member":
            date = input("Enter practice date (YYYY-MM-DD): ")
            time = input("Enter practice time: ")
            fee = self.SESSION_FEE  # Default fee for each session
            print(f"Session fee: ${fee}")
            amount_paid = float(input("Enter amount to pay: "))
            if amount_paid < fee:
                print("Amount paid is less than the session fee.")
            elif amount_paid >= fee:
                amount_due = amount_paid - fee
                member.add_payment(fee, str(datetime.now().date()))  # Record payment
                print("Payment successful.")
                if amount_due > 0:
                    print(f"Change due: ${amount_due}")
                    self.unpaid_debt[member.username] = self.unpaid_debt.get(member.username, 0) + amount_due
                    print("Unpaid debt recorded.")
            self.save_users_to_file()  # Save user information to file
        else:
            print("No members found.")

    def print_top_attendees(self, n=10):
        sorted_attendance = sorted(self.attendance.items(), key=lambda x: x[1], reverse=True)
        print("Top Attendees:")
        for i, (username, count) in enumerate(sorted_attendance[:n], start=1):
            print(f"{i}. {username}: {count} times")

    def send_practice_reminder(self):
        date = input("Enter practice date (YYYY-MM-DD): ")
        time = input("Enter practice time: ")
        location = input("Enter practice location: ")
        for user in self.users:
            if user.role == "Member":
                print(f"Reminder sent to {user.username}: Practice scheduled on {date} at {time} in {location}.")

    def track_club_finances(self):
        total_revenue = sum(self.payments.values()) + (len(self.users) * self.SESSION_FEE)  # Include session fees
        total_expenses = sum(self.expenses.values())  # Calculate total expenses
        # Print income statement
        print("Income Statement:")
        print(f"Total Revenue: ${total_revenue}")
        print(f"Total Expenses: ${total_expenses}")
        print(f"Net Profit: ${total_revenue - total_expenses}")

    def log_unpaid_debt(self):
        print("Unpaid Debt:")
        for username, amount in self.unpaid_debt.items():
            print(f"{username}: ${amount}")

    def current_month_account_payables(self):
        print("Current Month's Account Payables:")
        for username, amount in self.monthly_payables.items():
            print(f"{username}: ${amount}")

    def send_payment_reminder(self):
        today = datetime.date.today()
        for user in self.users:
            if user.role == "Member":
                if user.payment_status == "Unpaid" or self.is_due_today(user):
                    print(f"Payment reminder sent to {user.username}.")

    def is_due_today(self, user):
        for payment in user.payment_history:
            payment_date = datetime.strptime(payment["date"], "%Y-%m-%d").date()
            if payment_date == datetime.date.today():
                return True
        return False

    def refund(self, member_username, amount):
        for user in self.users:
            if user.username == member_username:
                if user.payment_status == "Paid":
                    user.add_payment(-amount, str(datetime.date.today()))
                    print(f"Refund of ${amount} processed for {member_username}.")
                else:
                    print(f"{member_username} has no payments to refund.")
                break
        else:
            print(f"Member '{member_username}' not found.")

    def log_and_sort_members(self):
        # Logging member attendance
        for user in self.users:
            if user.role == "Member" and user.attendance_count > 0:
                self.attendance[user.username] = user.attendance_count

        # Sort members by attendance
        sorted_members = sorted(self.attendance.items(), key=lambda x: x[1], reverse=True)
        print("Sorted Members by Attendance:")
        for username, count in sorted_members:
            print(f"{username}: {count} times")

    def update_payment_status(self):
        for user in self.users:
            if user.role == "Member":
                if user.payment_status == "Unpaid":
                    if user.attendance_count >= 3:  # If attended at least 3 times in a month
                        user.payment_status = "Paid"
                        user.add_payment(self.SESSION_FEE, str(datetime.now().date()))  # Record payment
                        print(f"Payment processed for {user.username}.")
                    else:
                        print(f"{user.username} still has unpaid dues.")
                elif user.payment_status == "Paid" and user.attendance_count < 3:
                    print(f"{user.username} has paid but attended less than 3 times.")

    # Add user interfaces for different roles

    def send_notification(self, sender, receiver, message):
        receiver.receive_notification(message)

if __name__ == "__main__":
    club = Club()
    club.load_users_from_file()  # Load existing user data

    while True:
        print("\nWelcome to the Membership Management System!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            club.register_member()

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = next((user for user in club.users if user.username == username and user.password == password), None)
            if user:
                if user.role == "Coach":
                    while True:
                        print("\nCoach Menu:")
                        print("1. Schedule Practice")
                        print("2. Logout")
                        coach_choice = input("Enter your choice (1-2): ")
                        if coach_choice == "1":
                            club.schedule_practice(user)
                        elif coach_choice == "2":
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice. Please try again.")
                elif user.role == "Treasurer":
                    while True:
                        print("\nTreasurer Menu:")
                        print("1. Manage Coach List")
                        print("2. Manage Schedule")
                        print("3. Track Club Finances")
                        print("4. Log Unpaid Debt")
                        print("5. Current Month's Account Payables")
                        print("6. Logout")
                        treasurer_choice = input("Enter your choice (1-6): ")
                        if treasurer_choice == "1":
                            club.manage_coach_list(user)
                        elif treasurer_choice == "2":
                            club.manage_schedule(user)
                        elif treasurer_choice == "3":
                            club.track_club_finances()
                        elif treasurer_choice == "4":
                            club.log_unpaid_debt()
                        elif treasurer_choice == "5":
                            club.current_month_account_payables()
                        elif treasurer_choice == "6":
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice. Please try again.")
                elif user.role == "Member":
                    while True:
                        print("\nMember Menu:")
                        print("1. View Scheduled Practices")
                        print("2. Schedule and Pay for Practice")
                        print("3. Logout")
                        member_choice = input("Enter your choice (1-3): ")
                        if member_choice == "1":
                            # Show scheduled practices
                            print("Scheduled Practices:")
                            for date, details in club.practice_schedule.items():
                                print(f"Date: {date}, Time: {details['time']}, Location: {details['location']}, Coach: {details['coach']}")
                        elif member_choice == "2":
                            club.members_schedule_and_pay_for_practice(user)
                        elif member_choice == "3":
                            print("Logging out...")
                            break  # Exiting the member's menu loop
                        else:
                            print("Invalid choice. Please try again.")

        elif choice == "3":
            print("Exiting...")
            club.save_users_to_file()  # Save user information before exiting
            break
        else:
            print("Invalid choice. Please try again.")
