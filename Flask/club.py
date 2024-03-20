import csv
from datetime import datetime
import ast
import json
import csv
import json

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
    SESSION_FEE = 10

    def __init__(self):
        self.users = []
        self.attendance = {}
        self.payments = {}
        self.unpaid_debt = {}
        self.coaches = []
        self.practice_schedule = {}
        self.expenses = {}
        self.monthly_payables = {}

    def load_users_from_csv(self):
        try:
            with open('users.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    payment_history_str = row.get('payment_history', '[]')
                    payment_history = json.loads(payment_history_str)
                    user = User(
                        row['username'], row['password'], row['role'], row['email'], row['phone'],
                        row.get('name'), row.get('address'), row.get('payment_preferences'),
                        row.get('payment_status'), int(row.get('attendance_count', 0)),
                        eval(row.get('notification_preferences', '{}')), payment_history
                    )
                    self.users.append(user)
                    if row['role'] == 'Coach':
                        self.coaches.append({'name': row['username'], 'contact_info': row['email']})
        except FileNotFoundError:
            print("No existing user data found.")

    def save_users_to_csv(self):
        with open('users.csv', mode='w', newline='') as file:
            fieldnames = ['username', 'password', 'role', 'email', 'phone', 'name', 'address', 'payment_preferences', 'payment_status', 'attendance_count', 'notification_preferences', 'payment_history']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for user in self.users:
                writer.writerow({
                    'username': user.username,
                    'password': user.password,
                    'role': user.role,
                    'email': user.email,
                    'phone': user.phone,
                    'name': user.name,
                    'address': user.address,
                    'payment_preferences': user.payment_preferences,
                    'payment_status': user.payment_status,
                    'attendance_count': user.attendance_count,
                    'notification_preferences': user.notification_preferences,
                    'payment_history': json.dumps(user.payment_history)  
                })


    def schedule_practice(self, coach, date, time, location):
        self.practice_schedule.setdefault(coach, []).append({'date': date, 'time': time, 'location': location})

    def get_scheduled_practices(self):
        return self.practice_schedule
